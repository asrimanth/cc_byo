# wc Clone

This is a simple implementation of the `wc` command in Python. It counts the number of lines, words, and characters in a given text file.

## Usage

For a single file:

```python
python ccwc.py <file_path>
```

For multiple files:

```python
python ccwc.py <file_path1> <file_path2> <file_path3> ...
```

For standard input (pipe or tree in linux):

```python
cat <file_path> | python ccwc.py
```

Flags:

- `-l` or `--lines`: Count lines
- `-w` or `--words`: Count words
- `-b` or `--bytes`: Count bytes
- `-c` or `--characters`: Count characters

**Defaults to count lines, words, bytes, and characters.**

## Implementation details

- The implementation uses a chunk size of 1MB for efficient reading of large files.
- Each function reads the file in chunks and counts the number of lines, words, bytes, and characters in each chunk.
- The total counts are then accumulated and printed at the end.
- Uses temporary files (also filled with chunks) for reading from stdin to avoid buffering issues.
