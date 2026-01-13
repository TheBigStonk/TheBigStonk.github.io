#!/usr/bin/env python3
import os
import re
from pathlib import Path
from html.parser import HTMLParser

class SimpleHTMLToMarkdownConverter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.skip_until_content = True
        self.found_content_start = False
        self.skip_nav = False
        self.skip_footer = False
        self.skip_layout_title = False
        self.in_paragraph = False
        self.in_heading = False
        self.heading_level = 0
        self.in_code = False
        self.in_samp = False
        self.in_em = False
        self.in_strong = False
        self.in_blockquote = False
        self.in_list = False
        self.list_item = False
        self.href = None
        self.title = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'body':
            self.skip_until_content = False
            self.found_content_start = True
            return

        # If we hit an H1 or H2 after head, start processing
        if tag in ['h1', 'h2'] and not self.found_content_start:
            self.skip_until_content = False
            self.found_content_start = True

        if self.skip_until_content and tag != 'head':
            return

        if tag == 'nav':
            self.skip_nav = True
            return
        elif tag == 'footer':
            self.skip_footer = True
            return

        if self.skip_nav or self.skip_footer:
            return

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_heading = True
            self.heading_level = int(tag[1])
            # Add newlines before heading
            if self.result and self.result[-1] != '\n':
                self.result.append('\n\n')
            self.result.append('#' * self.heading_level + ' ')

        elif tag == 'p':
            if not self.skip_layout_title:
                self.in_paragraph = True
                if self.result and self.result[-1] != '\n':
                    self.result.append('\n\n')

        elif tag == 'br':
            self.result.append('\n')

        elif tag == 'hr':
            self.result.append('\n\n---\n\n')

        elif tag in ['ul', 'ol']:
            self.in_list = True
            if self.result and self.result[-1] != '\n':
                self.result.append('\n')

        elif tag == 'li':
            self.list_item = True
            self.result.append('\n- ')

        elif tag == 'code':
            if not self.in_code:
                # Check if this is block code or inline code
                self.result.append('`')
                self.in_code = True

        elif tag == 'samp':
            if not self.in_samp:
                self.result.append('\n\n```\n')
                self.in_samp = True

        elif tag == 'a':
            self.href = attrs_dict.get('href', '')
            self.result.append('[')

        elif tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '')
            # Fix image paths
            src = src.replace('../images/', '/images/')
            src = src.replace('../', '/')
            self.result.append(f'\n\n![{alt}]({src})\n\n')

        elif tag in ['em', 'i']:
            self.in_em = True
            self.result.append('*')

        elif tag in ['strong', 'b']:
            self.in_strong = True
            self.result.append('**')

        elif tag == 'blockquote':
            self.in_blockquote = True
            self.result.append('\n\n> ')

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.skip_nav = False
            return
        elif tag == 'footer':
            self.skip_footer = False
            return

        if self.skip_nav or self.skip_footer or self.skip_until_content:
            return

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_heading = False
            self.heading_level = 0
            self.result.append('\n')

        elif tag == 'p':
            if self.in_paragraph:
                self.in_paragraph = False
                if self.skip_layout_title:
                    self.skip_layout_title = False

        elif tag in ['ul', 'ol']:
            self.in_list = False
            self.result.append('\n')

        elif tag == 'li':
            self.list_item = False

        elif tag == 'code':
            if self.in_code:
                self.result.append('`')
                self.in_code = False

        elif tag == 'samp':
            if self.in_samp:
                self.result.append('\n```\n\n')
                self.in_samp = False

        elif tag == 'a':
            if self.href:
                self.result.append(f']({self.href})')
                self.href = None

        elif tag in ['em', 'i']:
            if self.in_em:
                self.result.append('*')
                self.in_em = False

        elif tag in ['strong', 'b']:
            if self.in_strong:
                self.result.append('**')
                self.in_strong = False

        elif tag == 'blockquote':
            self.in_blockquote = False

    def handle_data(self, data):
        if self.skip_nav or self.skip_footer or self.skip_until_content:
            return

        # Check for layout/title marker
        if 'layout: post' in data:
            self.skip_layout_title = True
            return

        if 'title:' in data and self.skip_layout_title:
            # Extract title
            match = re.search(r'title:\s*(.+)', data)
            if match:
                self.title = match.group(1).strip()
            return

        # Skip "Max Francis - Cybersecurity" heading
        if self.in_heading and 'Max Francis' in data:
            return

        # For samp/code blocks, preserve whitespace
        if self.in_samp or self.in_code:
            # Just add data as-is for code blocks
            if data:
                self.result.append(data)
        else:
            # Add the data for normal content
            data = data.strip()
            if data:
                self.result.append(data)

    def get_markdown(self):
        # Join and clean up
        text = ''.join(self.result)
        # Clean up extra newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Fix code blocks that should be multiline
        text = re.sub(r'```\s*\n\s*', '\n```\n', text)
        return text.strip()

def convert_file(html_path, output_dir):
    """Convert a single HTML file to markdown"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse HTML
    parser = SimpleHTMLToMarkdownConverter()
    parser.feed(html_content)

    # Get title
    title = parser.title if parser.title else "Untitled"

    # Get markdown content
    markdown_content = parser.get_markdown()

    # Extract date from filename
    filename = os.path.basename(html_path)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        date_str = date_match.group(1)
        date = f"{date_str}T00:00:00+13:00"
    else:
        date = "2021-01-01T00:00:00+13:00"

    # Create front matter
    front_matter = f'''+++
title = "{title}"
date = "{date}"
draft = false
+++

'''

    # Combine
    full_content = front_matter + markdown_content

    # Output filename - KEEP THE DATE PREFIX
    output_filename = filename.replace('.html', '.md')
    output_path = os.path.join(output_dir, output_filename)

    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"[OK] Converted: {output_filename}")
    return output_path

def main():
    posts_dir = Path('posts-archived')
    output_dir = Path('content/posts')

    # Get all HTML files
    html_files = sorted(posts_dir.glob('*.html'))

    print(f"Found {len(html_files)} HTML files\n")

    # Skip already manually converted files
    skip_files = []

    converted = 0
    for html_file in html_files:
        if html_file.name in skip_files:
            print(f"[SKIP] {html_file.name} (already converted)")
            continue

        try:
            convert_file(html_file, output_dir)
            converted += 1
        except Exception as e:
            print(f"[ERROR] converting {html_file.name}: {e}")

    print(f"\n{converted} files converted successfully!")

if __name__ == '__main__':
    main()
