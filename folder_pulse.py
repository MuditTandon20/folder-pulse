"""Summarize a directory without third-party dependencies."""
import argparse
from collections import Counter
import json
from pathlib import Path


def scan(root):
    root = Path(root)
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    files, skipped = [], 0
    def on_error(_):
        nonlocal skipped
        skipped += 1
    import os
    for directory, _, names in os.walk(root, onerror=on_error, followlinks=False):
        for name in names:
            path = Path(directory) / name
            try:
                if path.is_symlink():
                    continue
                files.append((path.relative_to(root).as_posix(), path.stat().st_size))
            except OSError:
                skipped += 1
    return {
        "file_count": len(files),
        "total_bytes": sum(size for _, size in files),
        "extensions": dict(sorted(Counter(Path(name).suffix.lower() or "[no extension]" for name, _ in files).items())),
        "largest_files": [{"path": name, "bytes": size} for name, size in sorted(files, key=lambda item: (-item[1], item[0]))[:5]],
        "skipped_errors": skipped,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default=".")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()
    try:
        report = scan(args.directory)
    except ValueError as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Files: {report['file_count']} | Size: {report['total_bytes']:,} bytes")
        print("File types:")
        for extension, count in report["extensions"].items():
            print(f"  {extension}: {count}")
        print("Largest files:")
        for item in report["largest_files"]:
            print(f"  {item['path']}: {item['bytes']:,} bytes")
        print(f"Skipped errors: {report['skipped_errors']}")


if __name__ == "__main__":
    main()
