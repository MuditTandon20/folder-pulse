# Folder Pulse

A tiny Python CLI to see what is taking up space in a folder. No dependencies required; uses Python 3.10+.

## Run

```sh
python folder_pulse.py .
python folder_pulse.py /path/to/folder --json
```

Reports file count, total bytes, counts by extension, and the five largest files. Nested folders and hidden files are included. Symlinks are not followed. Unreadable entries are skipped and counted. Sizes are logical file sizes, not allocated disk usage. Hard links count separately. The scan stores one record per file in memory.

## Test

```sh
python -m unittest -v
```
