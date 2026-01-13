#!/usr/bin/env python3
import os
import re
from pathlib import Path
from html.parser import HTMLParser

class CleanHTMLToMarkdownConverter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.title = None
        self.skip_nav = False
        self.skip_footer = False
        self.skip_head = True
        self.skip_h1_max_francis = False
        self.in_paragraph = False
        self.in_heading = False
        self.heading_level = 0
        self.in_code = False
        self.in_samp = False
        self.in_em = False
        self.in_strong = False
        self.in_blockquote = False
        self.in_list = False
        self.href = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'head':
            self.skip_head = True
            return
        elif tag == 'body':
            self.skip_head = False
            return
        elif tag == 'nav':
            self.skip_nav = True
            return
        elif tag == 'footer':
            self.skip_footer = True
            return

        if self.skip_head or self.skip_nav or self.skip_footer:
            return

        if tag == 'h1':
            self.in_heading = True
            self.heading_level = 1
            self.skip_h1_max_francis = True
            return
        elif tag in ['h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_heading = True
            self.heading_level = int(tag[1])
            if self.result and self.result[-1] != '\n':
                self.result.append('\n\n')
            self.result.append('#' * self.heading_level + ' ')
        elif tag == 'p':
            self.in_paragraph = True
            if self.result and self.result[-1] != '\n':
                self.result.append('\n\n')
        elif tag == 'br':
            self.result.append('\n')
        elif tag == 'hr':
            # Skip HR tags entirely
            pass
        elif tag in ['ul', 'ol']:
            self.in_list = True
            if self.result and self.result[-1] != '\n':
                self.result.append('\n')
        elif tag == 'li':
            self.result.append('\n- ')
        elif tag == 'code':
            self.in_code = True
            self.result.append('`')
        elif tag == 'samp':
            self.in_samp = True
            self.result.append('\n\n```\n')
        elif tag == 'a':
            self.href = attrs_dict.get('href', '')
            self.result.append('[')
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '')
            # Fix image paths
            src = src.replace('../images/', '/images/')
            src = src.replace('../', '/')
            # Add spacing around images
            if self.result and self.result[-1] != '\n':
                self.result.append('\n\n')
            self.result.append(f'![{alt}]({src})')
            self.result.append('\n\n')
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
        if tag == 'head':
            self.skip_head = False
            return
        elif tag == 'nav':
            self.skip_nav = False
            return
        elif tag == 'footer':
            self.skip_footer = False
            return

        if self.skip_head or self.skip_nav or self.skip_footer:
            return

        if tag == 'h1':
            self.in_heading = False
            self.skip_h1_max_francis = False
        elif tag in ['h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_heading = False
            self.result.append('\n')
        elif tag == 'p':
            self.in_paragraph = False
        elif tag in ['ul', 'ol']:
            self.in_list = False
            self.result.append('\n')
        elif tag == 'code':
            self.in_code = False
            self.result.append('`')
        elif tag == 'samp':
            self.in_samp = False
            self.result.append('\n```\n')
        elif tag == 'a':
            if self.href:
                self.result.append(f']({self.href})')
                self.href = None
        elif tag in ['em', 'i']:
            self.in_em = False
            self.result.append('*')
        elif tag in ['strong', 'b']:
            self.in_strong = False
            self.result.append('**')
        elif tag == 'blockquote':
            self.in_blockquote = False

    def handle_data(self, data):
        if self.skip_head or self.skip_nav or self.skip_footer:
            return

        # Check for title in the "layout: post\ntitle: X" pattern
        if 'layout: post' in data or 'layout:post' in data:
            return
        if 'title:' in data and not self.title:
            match = re.search(r'title:\s*(.+?)(?:\n|$)', data)
            if match:
                self.title = match.group(1).strip()
            return

        # Skip Max Francis heading
        if self.skip_h1_max_francis:
            return

        # For code blocks, preserve formatting
        if self.in_samp:
            # Replace <br> with newlines in code
            data = data.replace('<br>', '\n')
            self.result.append(data)
        else:
            # Normal text - clean up whitespace
            # Replace multiple spaces/tabs with single space
            data = re.sub(r'\s+', ' ', data)
            data = data.strip()
            if data:
                self.result.append(data)

    def get_markdown(self):
        # Join result
        text = ''.join(self.result)

        # Clean up excessive newlines (more than 2 consecutive)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Clean up spaces before newlines
        text = re.sub(r' +\n', '\n', text)

        # Clean up markdown list formatting
        text = re.sub(r'\n- +', '\n- ', text)

        # Clean up multiple spaces
        text = re.sub(r'  +', ' ', text)

        # Fix spacing around links - remove double spaces
        text = re.sub(r'\) +([a-z])', r') \1', text)
        text = re.sub(r'\)  +', r') ', text)

        # Clean up blank lines in code blocks
        text = re.sub(r'```\n\n+', '```\n', text)
        text = re.sub(r'\n\n+```', '\n```', text)

        # Fix inline lists - convert "text: - item1; - item2; - item3" to proper lists
        # Look for patterns like ": - " and convert to newlines
        text = re.sub(r':\s*-\s+', ':\n\n- ', text)
        text = re.sub(r';\s*-\s+', '\n- ', text)
        text = re.sub(r';\s+and\s+-\s+', '\n- ', text)

        # Fix spacing issues around links
        text = re.sub(r'\)([a-zA-Z])', r') \1', text)  # Space after link
        text = re.sub(r'([a-z])\[', r'\1 [', text)  # Space before link

        return text.strip()

def convert_html_file(html_path, output_dir):
    """Convert a single HTML file to markdown"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extract title directly from HTML content before parsing
    title_match = re.search(r'title:\s*([^\n<]+)', html_content, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        # Try to find h2 or h3 as title
        h2_match = re.search(r'<h2[^>]*>([^<]+)</h2>', html_content)
        h3_match = re.search(r'<h3[^>]*>([^<]+)</h3>', html_content)
        if h2_match:
            title = h2_match.group(1).strip()
        elif h3_match:
            title = h3_match.group(1).strip()
        else:
            title = "Untitled Post"

    # Parse HTML
    parser = CleanHTMLToMarkdownConverter()
    parser.feed(html_content)

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

    # Create front matter (NO BOM)
    front_matter = f'+++\ntitle = "{title}"\ndate = "{date}"\ndraft = false\n+++\n\n'

    # Combine
    full_content = front_matter + markdown_content

    # Output filename - KEEP THE DATE PREFIX
    output_filename = filename.replace('.html', '.md')
    output_path = os.path.join(output_dir, output_filename)

    # Write file WITHOUT BOM
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"Converted: {output_filename} - '{title}'")
    return output_path

def main():
    posts_dir = Path('posts-archived')
    output_dir = Path('content/posts')

    # Get all HTML files
    html_files = sorted(posts_dir.glob('*.html'))

    print(f"Converting {len(html_files)} HTML files...\n")

    converted = 0
    for html_file in html_files:
        try:
            convert_html_file(html_file, output_dir)
            converted += 1
        except Exception as e:
            print(f"ERROR converting {html_file.name}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\nSuccessfully converted {converted}/{len(html_files)} files!")

if __name__ == '__main__':
    main()
