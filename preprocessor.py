#!/usr/bin/env python3
"""
mdBook Preprocessor: Custom Block Handler
Converts |||type syntax into HTML container divs.
"""

import sys
import json
import re

# Regex patterns
BLOCK_START_RE = re.compile(r"^\|\|\|([a-z-]+)$")
BLOCK_END_RE = re.compile(r"^\|\|\|$")

class BlockPreprocessor:
    def __init__(self):
        self.in_block = False

    def generate_html_header(self, block_type):
        """Returns the opening HTML structure for a custom block."""
        return [
            "",
            f'<div class="{block_type} container">',
            f'  <header><span class="{block_type}-title"></span></header>',
            '  <div class="container-content">',
            ""
        ]

    def generate_html_footer(self):
        """Returns the closing HTML structure for a custom block."""
        return ["", "  </div>", "</div>", ""]

    def process_content(self, content):
        """Parses markdown lines and injects HTML wrappers."""
        lines = content.split('\n')
        processed_lines = []
        self.in_block = False

        for line in lines:
            if not self.in_block:
                match = BLOCK_START_RE.match(line)
                if match:
                    processed_lines.extend(self.generate_html_header(match.group(1)))
                    self.in_block = True
                else:
                    processed_lines.append(line)
            else:
                if BLOCK_END_RE.match(line):
                    processed_lines.extend(self.generate_html_footer())
                    self.in_block = False
                else:
                    processed_lines.append(line)

        return "\n".join(processed_lines)

    def process_book_items(self, items):
        """Recursively processes chapters and sub-items."""
        for item in items:
            if 'Chapter' in item:
                chapter = item['Chapter']
                chapter['content'] = self.process_content(chapter['content'])
                
                # Recursive call to handle any level of nesting
                if chapter.get('sub_items'):
                    self.process_book_items(chapter['sub_items'])

def main():
    # Handle mdBook's capability check
    if len(sys.argv) > 1 and sys.argv[1] == 'supports':
        sys.exit(0)

    try:
        # Load book data from stdin
        context, book = json.load(sys.stdin)
        
        processor = BlockPreprocessor()
        processor.process_book_items(book['sections'])

        # Output transformed book to stdout
        json.dump(book, sys.stdout)
        
    except (EOFError, json.JSONDecodeError):
        sys.exit(1)

if __name__ == "__main__":
    main()