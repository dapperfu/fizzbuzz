#!/usr/bin/env python3
"""
Fix StrictDoc HTML paths to use relative paths.

This script converts absolute paths in StrictDoc-generated HTML files
to relative paths, making them work correctly from any folder location.
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Optional


def calculate_relative_path(from_file: Path, to_target: Path) -> str:
    """
    Calculate relative path from a file to a target path.
    
    Parameters
    ----------
    from_file : Path
        Path to the source file
    to_target : Path
        Path to the target (file or directory)
        
    Returns
    -------
    str
        Relative path from from_file to to_target
    """
    from_dir = from_file.parent
    try:
        rel_path = os.path.relpath(to_target, from_dir)
        # Normalize path separators for web (always use /)
        return str(rel_path).replace('\\', '/')
    except ValueError:
        # If paths are on different drives (Windows), return absolute path
        return str(to_target).replace('\\', '/')


def fix_paths_in_file(file_path: Path, strictdoc_dir: Path) -> None:
    """
    Fix paths in an HTML file, converting absolute paths to relative paths.
    
    Parameters
    ----------
    file_path : Path
        Path to the HTML file to fix
    strictdoc_dir : Path
        Path to the strictdoc output directory (contains _static and index.html)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Calculate relative paths from this file to key directories/files
    static_dir = strictdoc_dir / "_static"
    index_file = strictdoc_dir / "index.html"
    strictdoc_source_dir = strictdoc_dir / "strictdoc-source"
    
    rel_to_static = calculate_relative_path(file_path, static_dir)
    rel_to_index = calculate_relative_path(file_path, index_file)
    rel_to_strictdoc_source = calculate_relative_path(file_path, strictdoc_source_dir)
    
    # Ensure paths end with / for directories
    if rel_to_static and not rel_to_static.endswith('/'):
        rel_to_static += '/'
    if rel_to_strictdoc_source and not rel_to_strictdoc_source.endswith('/'):
        rel_to_strictdoc_source += '/'
    
    # Pattern to match absolute paths starting with /[repo]/strictdoc/ or any base path
    # This will match patterns like /fizzbuzz/strictdoc/_static/base.css
    # Match: /[anything]/strictdoc/ followed by the resource path
    abs_base_pattern = r'/[^/"\'>\s]+/strictdoc/'
    
    # Fix href attributes with absolute paths to _static/
    # Pattern: href="/fizzbuzz/strictdoc/_static/base.css"
    content = re.sub(
        r'href="' + abs_base_pattern + r'_static/',
        f'href="{rel_to_static}',
        content
    )
    
    # Fix src attributes with absolute paths to _static/
    # Pattern: src="/fizzbuzz/strictdoc/_static/stimulus_umd.min.js"
    content = re.sub(
        r'src="' + abs_base_pattern + r'_static/',
        f'src="{rel_to_static}',
        content
    )
    
    # Fix href attributes with absolute paths to index.html
    # Pattern: href="/fizzbuzz/strictdoc/index.html"
    content = re.sub(
        r'href="' + abs_base_pattern + r'index\.html',
        f'href="{rel_to_index}',
        content
    )
    
    # Fix href attributes with absolute paths to strictdoc-source/
    # Pattern: href="/fizzbuzz/strictdoc/strictdoc-source/FizzBuzz.html"
    content = re.sub(
        r'href="' + abs_base_pattern + r'strictdoc-source/',
        f'href="{rel_to_strictdoc_source}',
        content
    )
    
    # Fix absolute paths in data-path attributes (anchors)
    # Pattern: data-path="/fizzbuzz/strictdoc/#REQ-001"
    if file_path.parent == strictdoc_dir:
        # File is in root, use # directly
        content = re.sub(
            r'data-path="' + abs_base_pattern + r'#',
            'data-path="#',
            content
        )
    else:
        # File is in subdirectory, use ../#
        content = re.sub(
            r'data-path="' + abs_base_pattern + r'#',
            'data-path="../#',
            content
        )
    
    # Fix absolute paths in content attributes (meta tags)
    # Pattern: content="/fizzbuzz/strictdoc/_static/static_html_search_index.js"
    content = re.sub(
        r'content="' + abs_base_pattern + r'_static/',
        f'content="{rel_to_static}',
        content
    )
    
    # Fix rel="shortcut icon" href attributes
    # Pattern: href="/fizzbuzz/strictdoc/_static/favicon.ico"
    content = re.sub(
        r'(rel="shortcut icon"\s+href=")' + abs_base_pattern + r'_static/',
        r'\1' + rel_to_static,
        content
    )
    
    # Fix absolute file system paths (like /home/jed/fizzbuzz/docs/strictdoc-source)
    # Convert to relative path
    repo_root = strictdoc_dir.parent.parent
    repo_root_str = str(repo_root)
    
    # Replace absolute paths that contain repo root + /docs/strictdoc-source
    content = re.sub(
        re.escape(repo_root_str) + r'/docs/strictdoc-source',
        'strictdoc-source',
        content
    )
    
    # Handle any absolute Unix-style path ending with /docs/strictdoc-source
    content = re.sub(
        r'/[^"\'<>]*/docs/strictdoc-source',
        'strictdoc-source',
        content
    )
    
    # Fix any remaining broken paths
    content = re.sub(
        re.escape(repo_root_str) + r'strictdoc-source',
        'strictdoc-source',
        content
    )
    
    content = re.sub(
        r'/[^"\'<>]*strictdoc-source',
        'strictdoc-source',
        content
    )
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed paths in: {file_path}")


def fix_strictdoc_paths(strictdoc_dir: Path) -> None:
    """
    Fix all HTML files in the StrictDoc output directory.
    
    Parameters
    ----------
    strictdoc_dir : Path
        Path to the StrictDoc output directory
    """
    html_files: List[Path] = []
    
    # Find all HTML files
    for root, dirs, files in os.walk(strictdoc_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    
    print(f"Found {len(html_files)} HTML files to process")
    
    for html_file in html_files:
        fix_paths_in_file(html_file, strictdoc_dir)
    
    print(f"Finished fixing paths in {len(html_files)} files")


def get_repo_name(repo_path: Path) -> str:
    """
    Get the repository name from git remote or directory name.
    
    Parameters
    ----------
    repo_path : Path
        Path to the repository root
        
    Returns
    -------
    str
        Repository name
    """
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            # Extract repo name from git URL
            url = result.stdout.strip()
            # Match patterns like:
            # - https://github.com/user/repo.git
            # - git@github.com:user/repo.git
            # - https://github.com/user/repo
            match = re.search(r'github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$', url)
            if match:
                repo_name = match.group(2)
                return repo_name
    except Exception:
        pass
    
    # Fallback to directory name
    return repo_path.name


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    strictdoc_dir = script_dir / "docs" / "strictdoc"
    
    if not strictdoc_dir.exists():
        print(f"Error: StrictDoc directory not found at {strictdoc_dir}")
        exit(1)
    
    print(f"StrictDoc directory: {strictdoc_dir}")
    print("Converting absolute paths to relative paths...")
    
    fix_strictdoc_paths(strictdoc_dir)

