#!/usr/bin/env python3
"""
Release automation script for BAUERGROUP S3 Compatible Backup Integration.

This script automates the release process by:
1. Validating version format
2. Updating version in all relevant files
3. Creating git commit and tag
4. Pushing to remote repository

Usage:
    python release.py [version]
    python release.py 0.1.1

If no version is provided, it will prompt for one.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

    @classmethod
    def supports_color(cls) -> bool:
        """Check if terminal supports colors."""
        return (
            hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() and
            os.environ.get('TERM') != 'dumb'
        )


def print_success(message: str) -> None:
    """Print success message in green."""
    if Colors.supports_color():
        print(f"{Colors.GREEN}✓ {message}{Colors.NC}")
    else:
        print(f"[OK] {message}")


def print_error(message: str) -> None:
    """Print error message in red."""
    if Colors.supports_color():
        print(f"{Colors.RED}✗ {message}{Colors.NC}")
    else:
        print(f"[ERROR] {message}")


def print_info(message: str) -> None:
    """Print info message in yellow."""
    if Colors.supports_color():
        print(f"{Colors.YELLOW}ℹ {message}{Colors.NC}")
    else:
        print(f"[INFO] {message}")


def print_step(message: str) -> None:
    """Print step message in blue."""
    if Colors.supports_color():
        print(f"{Colors.BLUE}▶ {message}{Colors.NC}")
    else:
        print(f">>> {message}")


def run_command(cmd: list[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    """
    Run a shell command.

    Args:
        cmd: Command to run as list of arguments
        check: Whether to raise exception on non-zero exit code
        capture: Whether to capture output

    Returns:
        CompletedProcess object
    """
    try:
        if capture:
            result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, check=check)
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(cmd)}")
        if e.stderr:
            print(e.stderr)
        raise


def validate_version(version: str) -> bool:
    """
    Validate version format (semantic versioning).

    Args:
        version: Version string to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version))


def check_git_status() -> bool:
    """
    Check if there are uncommitted changes.

    Returns:
        True if working directory is clean, False otherwise
    """
    result = run_command(['git', 'diff-index', '--quiet', 'HEAD', '--'], check=False)
    return result.returncode == 0


def get_current_branch() -> str:
    """Get current git branch name."""
    result = run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    return result.stdout.strip()


def tag_exists(tag: str) -> bool:
    """Check if a git tag exists."""
    result = run_command(['git', 'rev-parse', tag], check=False)
    return result.returncode == 0


def update_manifest_version(version: str) -> None:
    """
    Update version in manifest.json.

    Args:
        version: New version string
    """
    manifest_path = Path('custom_components/bauergroup_s3compatiblebackup/manifest.json')

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    manifest['version'] = version

    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write('\n')  # Add newline at end of file

    print_success(f"Updated {manifest_path}")


def find_all_markdown_files() -> list[Path]:
    """
    Find all *.md files in the project.

    Returns:
        List of Path objects for all markdown files
    """
    project_root = Path('.')
    md_files = []

    # Find all .md files recursively, excluding hidden directories and node_modules
    for md_file in project_root.rglob('*.md'):
        # Skip hidden directories (starting with .)
        if any(part.startswith('.') for part in md_file.parts):
            continue
        # Skip node_modules
        if 'node_modules' in md_file.parts:
            continue
        md_files.append(md_file)

    return md_files


def update_markdown_file_version(file_path: Path, version: str) -> bool:
    """
    Update version references in a markdown file.

    Args:
        file_path: Path to markdown file
        version: New version string

    Returns:
        True if file was modified, False otherwise
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    content = original_content

    # Pattern 1: **Version:** X.X.X
    content = re.sub(
        r'\*\*Version:\*\* \d+\.\d+\.\d+',
        f'**Version:** {version}',
        content
    )

    # Pattern 2: Version: X.X.X (without bold)
    content = re.sub(
        r'(?<![\*])Version: \d+\.\d+\.\d+',
        f'Version: {version}',
        content
    )

    # Pattern 3: Version badge in shields.io
    content = re.sub(
        r'!\[Version\]\(https://img\.shields\.io/badge/version-\d+\.\d+\.\d+',
        f'![Version](https://img.shields.io/badge/version-{version}',
        content
    )

    # Pattern 4: GitHub release badge
    content = re.sub(
        r'!\[GitHub Release\]\(https://img\.shields\.io/github/v/release/[^)]+\)',
        f'![GitHub Release](https://img.shields.io/github/v/release/bauer-group/IP-HomeassistantS3CompatibleBackup?style=for-the-badge)',
        content
    )

    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def update_all_versions(version: str) -> list[Path]:
    """
    Update version in all relevant files.

    Args:
        version: New version string

    Returns:
        List of updated file paths
    """
    print_step(f"Updating version to {version} in all files...")

    updated_files = []

    # Update manifest.json
    update_manifest_version(version)
    updated_files.append(Path('custom_components/bauergroup_s3compatiblebackup/manifest.json'))

    # Find and update all markdown files
    print_step("Scanning for markdown files...")
    md_files = find_all_markdown_files()
    print_success(f"Found {len(md_files)} markdown files")

    for md_file in md_files:
        if update_markdown_file_version(md_file, version):
            print_success(f"Updated {md_file}")
            updated_files.append(md_file)
        else:
            print_info(f"No version references found in {md_file}")

    return updated_files


def extract_changelog_section(version: str) -> Optional[str]:
    """
    Extract the changelog section for a specific version.

    Args:
        version: Version string (e.g., "0.2.4")

    Returns:
        Changelog section content or None if not found
    """
    changelog_path = Path('CHANGELOG.md')

    if not changelog_path.exists():
        return None

    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match version section: ## [X.X.X] - YYYY-MM-DD
    # and capture everything until the next version section or end
    pattern = rf'## \[{re.escape(version)}\][^\n]*\n(.*?)(?=\n## \[|\Z)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        section = match.group(1).strip()
        return section

    return None


def create_github_release(version: str) -> bool:
    """
    Create a GitHub release using gh CLI.

    Args:
        version: Version string (e.g., "0.1.1")

    Returns:
        True if successful, False otherwise
    """
    tag_name = f"v{version}"

    print_step("Creating GitHub release...")

    # Check if gh CLI is available
    result = run_command(['gh', '--version'], check=False)
    if result.returncode != 0:
        print_error("GitHub CLI (gh) not found. Please install it from: https://cli.github.com/")
        print_info("You can create the release manually at:")
        print(f"  https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/releases/new?tag={tag_name}")
        return False

    # Try to extract changelog section for this version
    changelog_section = extract_changelog_section(version)

    if changelog_section:
        print_success(f"Found changelog section for v{version}")
        release_notes = changelog_section
    else:
        print_info(f"No changelog section found for v{version}, using default text")
        release_notes = f"""Version bump to v{version}

See [CHANGELOG.md](https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/blob/main/CHANGELOG.md) for details."""

    release_title = f"v{version}"

    # Create release
    try:
        result = run_command([
            'gh', 'release', 'create', tag_name,
            '--title', release_title,
            '--notes', release_notes
        ], check=True, capture=False)

        print_success(f"Created GitHub release: {tag_name}")
        print_info(f"View release at: https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/releases/tag/{tag_name}")
        return True

    except subprocess.CalledProcessError:
        print_error("Failed to create GitHub release")
        print_info("You can create it manually at:")
        print(f"  https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/releases/new?tag={tag_name}")
        return False


def create_release(version: str, push: bool = True, github_release: bool = True) -> None:
    """
    Create a release with the given version.

    Args:
        version: Version string (e.g., "0.1.1")
        push: Whether to push to remote
    """
    print()
    print_info(f"Starting release process for version v{version}")
    print()

    # Validate version format
    if not validate_version(version):
        print_error(f"Invalid version format: {version}")
        print_error("Version must follow semantic versioning (e.g., 0.1.0)")
        sys.exit(1)

    # Check for uncommitted changes
    if not check_git_status():
        print_error("You have uncommitted changes. Please commit or stash them first.")
        run_command(['git', 'status', '--short'], capture=False)
        sys.exit(1)

    print_success("No uncommitted changes found")
    print()

    # Update all version references
    updated_files = update_all_versions(version)
    print()

    # Stage all updated files
    print_step("Staging updated files...")
    for file_path in updated_files:
        run_command(['git', 'add', str(file_path)])
    print_success(f"Staged {len(updated_files)} files")
    print()

    # Commit changes
    print_step("Committing version bump...")
    commit_msg = f"chore: Bump version to v{version}"
    result = run_command(['git', 'commit', '-m', commit_msg], check=False)

    if result.returncode == 0:
        print_success(f"Created commit: {commit_msg}")
    else:
        print_info("No changes to commit (version already up to date)")
    print()

    # Handle existing tag
    tag_name = f"v{version}"
    if tag_exists(tag_name):
        print_error(f"Tag {tag_name} already exists!")
        response = input("Do you want to delete and recreate it? (y/n): ").strip().lower()
        if response == 'y':
            run_command(['git', 'tag', '-d', tag_name])
            print_success(f"Deleted existing tag {tag_name}")
        else:
            print_error("Aborted: Tag already exists")
            sys.exit(1)

    # Create tag
    print_step(f"Creating git tag {tag_name}...")
    tag_msg = f"Release version v{version}"
    run_command(['git', 'tag', '-a', tag_name, '-m', tag_msg])
    print_success(f"Created tag {tag_name}")
    print()

    # Push to remote
    if push:
        print_info("Ready to push to remote repository")
        print("This will push:")
        print(f"  - Latest commits to {get_current_branch()} branch")
        print(f"  - Tag {tag_name}")
        print()

        response = input("Continue? (y/n): ").strip().lower()

        if response == 'y':
            print_step("Pushing to remote...")
            print()

            # Push commits
            branch = get_current_branch()
            run_command(['git', 'push', 'origin', branch], capture=False)
            print_success(f"Pushed commits to {branch} branch")
            print()

            # Push tag
            run_command(['git', 'push', 'origin', tag_name], capture=False)
            print_success(f"Pushed tag {tag_name}")
            print()

            print_success(f"Release v{version} completed successfully!")
            print()

            # Create GitHub release
            if github_release:
                print()
                create_github_release(version)
                print()

            print_info("Next steps:")
            if not github_release:
                print(f"  1. Create a GitHub release at: https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/releases/new?tag={tag_name}")
                print("  2. Wait for HACS to recognize the new version")
                print("  3. Test installation via HACS")
            else:
                print("  1. Wait for HACS to recognize the new version (may take a few minutes)")
                print("  2. Test installation/update via HACS")
                print("  3. Verify integration works correctly")
        else:
            print_info("Push cancelled. You can push manually later with:")
            print(f"  git push origin {get_current_branch()}")
            print(f"  git push origin {tag_name}")
    else:
        print_info("Skipping push (use --push to push automatically)")
        print_info("You can push manually with:")
        print(f"  git push origin {get_current_branch()}")
        print(f"  git push origin {tag_name}")

    print()
    print_success("Done!")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Release automation script for BAUERGROUP S3 Compatible Backup Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python release.py 0.1.1
  python release.py 0.2.0 --no-push
  python release.py --help
        """
    )

    parser.add_argument(
        'version',
        nargs='?',
        help='Version number (e.g., 0.1.0)'
    )

    parser.add_argument(
        '--no-push',
        action='store_true',
        help='Do not push to remote (only create local commit and tag)'
    )

    parser.add_argument(
        '--no-github-release',
        action='store_true',
        help='Do not create GitHub release (only push tag)'
    )

    args = parser.parse_args()

    # Get version from argument or prompt
    version = args.version
    if not version:
        version = input("Enter version number (e.g., 0.1.0): ").strip()

    if not version:
        print_error("Version is required")
        sys.exit(1)

    # Create release
    try:
        create_release(
            version,
            push=not args.no_push,
            github_release=not args.no_github_release
        )
    except KeyboardInterrupt:
        print()
        print_error("Aborted by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Release failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
