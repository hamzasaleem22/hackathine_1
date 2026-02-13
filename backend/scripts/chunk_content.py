#!/usr/bin/env python3
"""
Chunk content by H2/H3 heading boundaries.

Splits extracted MDX content into semantic chunks based on heading structure,
preserving metadata for each chunk (module_id, chapter_id, section_id, etc.)
"""
import re
from typing import Dict, List
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from extract_content import extract_mdx_files


def chunk_by_headings(content: str, metadata: Dict) -> List[Dict]:
    """
    Split content into chunks based on H2/H3 headings.

    Args:
        content: The markdown content to chunk
        metadata: File-level metadata to attach to each chunk

    Returns:
        List of chunks with metadata
    """
    chunks = []

    # Split by H2 headings (##)
    h2_pattern = r'^## (.+)$'
    h2_splits = re.split(h2_pattern, content, flags=re.MULTILINE)

    # First element might be intro content before any heading
    intro_text = h2_splits[0].strip()
    if intro_text and len(intro_text) > 100:  # Only include if substantial
        chunks.append({
            'text': intro_text,
            'heading': metadata['title'],  # Use file title for intro
            'heading_level': 1,
            'section_id': 'intro',
            'metadata': metadata.copy()
        })

    # Process H2 sections
    for i in range(1, len(h2_splits), 2):
        if i + 1 >= len(h2_splits):
            break

        h2_heading = h2_splits[i].strip()
        h2_content = h2_splits[i + 1].strip()

        # Further split by H3 headings within this H2 section
        h3_pattern = r'^### (.+)$'
        h3_splits = re.split(h3_pattern, h2_content, flags=re.MULTILINE)

        # Content before first H3 (belongs to H2)
        h2_intro = h3_splits[0].strip()
        if h2_intro and len(h2_intro) > 50:
            chunks.append({
                'text': h2_intro,
                'heading': h2_heading,
                'heading_level': 2,
                'section_id': heading_to_id(h2_heading),
                'metadata': metadata.copy()
            })

        # Process H3 sections
        for j in range(1, len(h3_splits), 2):
            if j + 1 >= len(h3_splits):
                break

            h3_heading = h3_splits[j].strip()
            h3_content = h3_splits[j + 1].strip()

            if h3_content and len(h3_content) > 50:
                chunks.append({
                    'text': h3_content,
                    'heading': f"{h2_heading} > {h3_heading}",
                    'heading_level': 3,
                    'section_id': heading_to_id(h3_heading),
                    'parent_section': heading_to_id(h2_heading),
                    'metadata': metadata.copy()
                })

    return chunks


def heading_to_id(heading: str) -> str:
    """Convert heading text to URL-friendly ID."""
    # Remove special characters, convert to lowercase, replace spaces with hyphens
    id_str = re.sub(r'[^\w\s-]', '', heading.lower())
    id_str = re.sub(r'[\s_]+', '-', id_str)
    return id_str.strip('-')


def extract_images_and_captions(text: str) -> List[Dict]:
    """
    Extract image references with captions and alt-text from markdown.

    Args:
        text: Markdown text content

    Returns:
        List of image references with metadata
    """
    images = []

    # Pattern: ![alt text](url "caption")
    image_pattern = r'!\[([^\]]*)\]\(([^\)]+?)(?:\s+"([^"]+)")?\)'

    for match in re.finditer(image_pattern, text):
        alt_text = match.group(1).strip()
        url = match.group(2).strip()
        caption = match.group(3).strip() if match.group(3) else alt_text

        images.append({
            'alt_text': alt_text,
            'url': url,
            'caption': caption
        })

    return images


def process_all_files(docs_dir: str) -> List[Dict]:
    """
    Process all MDX files and create chunks.

    Args:
        docs_dir: Path to docs directory

    Returns:
        List of all chunks with metadata
    """
    print("=" * 60)
    print("✂️  Chunking Content by Headings")
    print("=" * 60)
    print()

    # Extract files
    files = extract_mdx_files(docs_dir)

    all_chunks = []
    total_images = 0

    for file_data in files:
        content = file_data['content']
        metadata = file_data['metadata']

        # Create chunks from content
        file_chunks = chunk_by_headings(content, metadata)

        # Extract images from each chunk
        for chunk in file_chunks:
            images = extract_images_and_captions(chunk['text'])
            chunk['image_references'] = images
            total_images += len(images)

        all_chunks.extend(file_chunks)

        print(f"  {metadata['relative_path']}: {len(file_chunks)} chunks")

    print()
    print("=" * 60)
    print("📊 Chunking Summary")
    print("=" * 60)
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Total images: {total_images}")

    # Calculate average chunk size
    if all_chunks:
        avg_size = sum(len(c['text']) for c in all_chunks) / len(all_chunks)
        print(f"Average chunk size: {int(avg_size)} characters")

    # Group by module
    modules = {}
    for chunk in all_chunks:
        module = chunk['metadata']['module_id']
        modules[module] = modules.get(module, 0) + 1

    print("\nChunks per module:")
    for module, count in sorted(modules.items()):
        print(f"  {module}: {count} chunks")

    return all_chunks


def main():
    """Main execution function."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    docs_dir = project_root / 'frontend' / 'docs'

    chunks = process_all_files(str(docs_dir))

    return chunks


if __name__ == "__main__":
    main()
