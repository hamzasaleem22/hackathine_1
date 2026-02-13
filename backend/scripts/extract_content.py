#!/usr/bin/env python3
"""
Extract content from MDX files in the Docusaurus frontend.

Parses MDX files from /frontend/docs/ and extracts:
- Frontmatter metadata (title, description, etc.)
- Body content (text, excluding code blocks if needed)
- File path and navigation structure
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Optional
import frontmatter


def extract_mdx_files(docs_dir: str) -> List[Dict]:
    """
    Extract all MDX files from the docs directory.

    Args:
        docs_dir: Path to the Docusaurus docs directory

    Returns:
        List of dictionaries containing extracted content and metadata
    """
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    extracted_content = []

    # Find all .md and .mdx files recursively
    for file_path in docs_path.rglob("*.md*"):
        if file_path.is_file():
            content_data = extract_single_file(file_path, docs_path)
            if content_data:
                extracted_content.append(content_data)

    print(f"✅ Extracted {len(extracted_content)} files from {docs_dir}")
    return extracted_content


def extract_single_file(file_path: Path, docs_root: Path) -> Optional[Dict]:
    """
    Extract content from a single MDX file.

    Args:
        file_path: Path to the MDX file
        docs_root: Root docs directory for relative path calculation

    Returns:
        Dictionary with file metadata and content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # Get relative path from docs root
        relative_path = file_path.relative_to(docs_root)

        # Parse module/chapter structure from path
        path_parts = list(relative_path.parts)

        # Extract module ID (e.g., "module-0" from path)
        module_id = None
        chapter_id = None

        for part in path_parts:
            if part.startswith('module-'):
                module_id = part
            elif part.startswith('chapter-') or part.startswith('ch-'):
                chapter_id = part

        # Build navigation URL (relative to /docs/)
        nav_url = '/' + str(relative_path).replace('\\', '/').replace('.mdx', '').replace('.md', '')

        # Extract metadata
        metadata = {
            'file_path': str(file_path),
            'relative_path': str(relative_path),
            'navigation_url': nav_url,
            'module_id': module_id or 'general',
            'chapter_id': chapter_id or 'intro',
            'title': post.get('title', path_parts[-1].replace('.mdx', '').replace('.md', '')),
            'description': post.get('description', ''),
            'sidebar_position': post.get('sidebar_position', 0),
        }

        # Get body content
        body_content = post.content.strip()

        return {
            'metadata': metadata,
            'content': body_content
        }

    except Exception as e:
        print(f"⚠️  Warning: Failed to parse {file_path}: {str(e)}")
        return None


def main():
    """Main execution function."""
    # Determine docs directory (relative to this script)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    docs_dir = project_root / 'frontend' / 'docs'

    print("=" * 60)
    print("📄 Extracting Content from MDX Files")
    print("=" * 60)
    print(f"Docs directory: {docs_dir}")
    print()

    # Extract all MDX files
    extracted = extract_mdx_files(str(docs_dir))

    # Print summary
    print()
    print("=" * 60)
    print("📊 Extraction Summary")
    print("=" * 60)
    print(f"Total files: {len(extracted)}")

    # Count by module
    modules = {}
    for item in extracted:
        module = item['metadata']['module_id']
        modules[module] = modules.get(module, 0) + 1

    print("\nFiles per module:")
    for module, count in sorted(modules.items()):
        print(f"  {module}: {count} files")

    return extracted


if __name__ == "__main__":
    main()
