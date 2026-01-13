#!/usr/bin/env python3
import os
import re
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime

class HTMLToMarkdownConverter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.markdown = []
        self.in_title = False
        self.in_body = False
        self.title = ""
        self.list_stack = []
        self.in_code = False
        self.in_blockquote = False
        self.current_tag_stack = []

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True
        elif not self.in_body:
            return

        self.current_tag_stack.append(tag)

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag[1])
            self.markdown.append('\n' + '#' * level + ' ')
        elif tag == 'p':
            if not self.in_title:
                self.markdown.append('\n')
        elif tag == 'br':
            self.markdown.append('\n')
        elif tag == 'hr':
            self.markdown.append('\n---\n')
        elif tag == 'ul':
            self.list_stack.append('ul')
        elif tag == 'ol':
            self.list_stack.append('ol')
        elif tag == 'li':
            self.markdown.append('\n- ')
        elif tag == 'code':
            if not self.in_code:
                self.markdown.append('```')
                self.in_code = True
        elif tag == 'a':
            href = dict(attrs).get('href', '')
            self.markdown.append('[')
            self.link_href = href
        elif tag == 'img':
            src = dict(attrs).get('src', '')
            alt = dict(attrs).get('alt', '')
            # Convert image paths
            src = src.replace('../images/', '/images/')
            src = src.replace('../', '/')
            self.markdown.append(f'\n![{alt}]({src})\n')
        elif tag == 'em' or tag == 'i':
            self.markdown.append('*')
        elif tag == 'strong' or tag == 'b':
            self.markdown.append('**')
        elif tag == 'blockquote':
            self.markdown.append('\n> ')
            self.in_blockquote = True

    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
            return
        elif not self.in_body:
            return

        if self.current_tag_stack and self.current_tag_stack[-1] == tag:
            self.current_tag_stack.pop()

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.markdown.append('\n')
        elif tag == 'p':
            self.markdown.append('\n')
        elif tag == 'ul' or tag == 'ol':
            if self.list_stack:
                self.list_stack.pop()
            self.markdown.append('\n')
        elif tag == 'code':
            if self.in_code:
                self.markdown.append('```')
                self.in_code = False
        elif tag == 'a':
            href = getattr(self, 'link_href', '')
            self.markdown.append(f']({href})')
        elif tag == 'em' or tag == 'i':
            self.markdown.append('*')
        elif tag == 'strong' or tag == 'b':
            self.markdown.append('**')
        elif tag == 'blockquote':
            self.in_blockquote = False

    def handle_data(self, data):
        if not self.in_body:
            return

        # Skip navigation and layout elements
        if 'layout: post' in data:
            self.in_title = True
            return
        if self.in_title and 'title:' in data:
            self.title = data.replace('title:', '').strip()
            self.in_title = False
            return

        # Clean up the data
        data = data.strip()
        if data:
            self.markdown.append(data)

    def get_markdown(self):
        return ''.join(self.markdown).strip()

def extract_title_from_html(html_content):
    """Extract title from HTML content"""
    # Look for "title: Something" pattern
    title_match = re.search(r'title:\s*([^\n<]+)', html_content)
    if title_match:
        return title_match.group(1).strip()
    return "Untitled"

def convert_html_to_markdown(html_file, output_dir):
    """Convert a single HTML file to markdown"""
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extract title
    title = extract_title_from_html(html_content)

    # Get date from filename
    filename = os.path.basename(html_file)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        date_str = date_match.group(1)
        date = f"{date_str}T00:00:00+13:00"
    else:
        date = "2021-01-01T00:00:00+13:00"

    # Convert HTML to Markdown
    parser = HTMLToMarkdownConverter()
    parser.feed(html_content)
    markdown_content = parser.get_markdown()

    # Clean up the markdown
    # Remove empty lines
    lines = markdown_content.split('\n')
    cleaned_lines = []
    for i, line in enumerate(lines):
        line = line.strip()
        if line or (i > 0 and cleaned_lines and cleaned_lines[-1]):
            cleaned_lines.append(line)

    # Join and clean up
    markdown_content = '\n'.join(cleaned_lines)

    # Remove the header/footer content
    markdown_content = re.sub(r'Max Francis - Cybersecurity.*?---', '', markdown_content, flags=re.DOTALL)
    markdown_content = re.sub(r'---\s*Max Francis - CC By Attribution', '', markdown_content)

    # Create the front matter
    front_matter = f'''+++
title = "{title}"
date = "{date}"
draft = false
+++

'''

    # Combine front matter and content
    full_markdown = front_matter + markdown_content.strip()

    # Create output filename
    output_filename = filename.replace('.html', '.md')
    output_path = os.path.join(output_dir, output_filename)

    # Write the markdown file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_markdown)

    print(f"Converted: {filename} -> {output_filename}")
    return output_path

def main():
    # Set up paths
    posts_archived_dir = Path('posts-archived')
    output_dir = Path('content/posts')

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all HTML files
    html_files = list(posts_archived_dir.glob('*.html'))

    # Skip files that have already been converted
    already_converted = ['2021-10-11-Hello-World.html',
                        '2021-10-17-PHP-Type-Vulnerabilities.html',
                        '2021-10-22-Username-Enumeration-in-Webapps.html',
                        '2021-10-29-Passing-The-PNPT.html']

    print(f"Found {len(html_files)} HTML files")
    print(f"Skipping {len(already_converted)} already converted files")

    # Convert each file
    converted_count = 0
    for html_file in html_files:
        if html_file.name in already_converted:
            print(f"Skipping: {html_file.name} (already converted)")
            continue

        try:
            convert_html_to_markdown(html_file, output_dir)
            converted_count += 1
        except Exception as e:
            print(f"Error converting {html_file.name}: {e}")

    print(f"\nConversion complete! Converted {converted_count} files.")

if __name__ == '__main__':
    main()
