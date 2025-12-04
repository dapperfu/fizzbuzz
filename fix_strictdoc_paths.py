#!/usr/bin/env python3
"""
Fix StrictDoc HTML paths for GitHub Pages compatibility.

This script converts relative paths in StrictDoc-generated HTML files
to absolute paths from the repository root, making them work correctly
when served on GitHub Pages.
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Optional


def fix_paths_in_file(file_path: Path, base_path: str) -> None:
    """
    Fix relative paths in an HTML file to use absolute paths from repo root.
    
    Parameters
    ----------
    file_path : Path
        Path to the HTML file to fix
    base_path : str
        Base path from repository root (e.g., "/docs/strictdoc")
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix href="../_static/ to href="/docs/strictdoc/_static/
    content = re.sub(
        r'href="\.\./_static/',
        f'href="{base_path}/_static/',
        content
    )
    
    # Fix src="../_static/ to src="/docs/strictdoc/_static/
    content = re.sub(
        r'src="\.\./_static/',
        f'src="{base_path}/_static/',
        content
    )
    
    # Fix href="../index.html to href="/docs/strictdoc/index.html
    content = re.sub(
        r'href="\.\./index\.html',
        f'href="{base_path}/index.html',
        content
    )
    
    # Fix href="../strictdoc-source/ to href="/docs/strictdoc/strictdoc-source/
    content = re.sub(
        r'href="\.\./strictdoc-source/',
        f'href="{base_path}/strictdoc-source/',
        content
    )
    
    # Fix data-path="../# to data-path="/docs/strictdoc/#
    content = re.sub(
        r'data-path="\.\./#',
        f'data-path="{base_path}/#',
        content
    )
    
    # Fix content="../_static/ to content="/docs/strictdoc/_static/
    content = re.sub(
        r'content="\.\./_static/',
        f'content="{base_path}/_static/',
        content
    )
    
    # Fix pathPrefix in JavaScript (for search functionality)
    # Look for patterns like pathPrefix + "index.html" or similar
    content = re.sub(
        r'pathPrefix\s*\+\s*["\']\.\./',
        f'pathPrefix + "{base_path}/',
        content
    )
    
    # Also fix paths that were already converted with wrong base path
    # Replace any /docs/strictdoc/ with the correct base_path
    content = re.sub(
        r'/docs/strictdoc/',
        f'{base_path}/',
        content
    )
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed paths in: {file_path}")


def fix_strictdoc_paths(strictdoc_dir: Path, base_path: str = "/docs/strictdoc") -> None:
    """
    Fix all HTML files in the StrictDoc output directory.
    
    Parameters
    ----------
    strictdoc_dir : Path
        Path to the StrictDoc output directory
    base_path : str
        Base path from repository root (default: "/docs/strictdoc")
    """
    html_files: List[Path] = []
    
    # Find all HTML files
    for root, dirs, files in os.walk(strictdoc_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    
    print(f"Found {len(html_files)} HTML files to process")
    
    for html_file in html_files:
        fix_paths_in_file(html_file, base_path)
    
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
    
    # Get repository name for GitHub Pages base path
    repo_name = get_repo_name(script_dir)
    base_path = f"/{repo_name}/strictdoc"
    print(f"Using base path: {base_path}")
    
    fix_strictdoc_paths(strictdoc_dir, base_path)

