"""
A simple module which replicates the functionality of the Unix wc command.
"""

import argparse
import os
import sys

# Set the chunk size to 1MB
# Helpful for large files
CHUNK_SIZE: int = 1024 * 1024


def count_lines(filepath: str) -> int:
    """Counts the number of lines in a file

    Args:
        filepath (str): The path to the file to count lines in

    Returns:
        int: The number of lines in the file
    """
    total_lines = 0

    with open(filepath, "r") as f:
        while True:
            chunk = f.readlines(CHUNK_SIZE)
            if not chunk:
                break
            total_lines += len(chunk)
    return total_lines


def count_words(filepath: str) -> int:
    """Counts the number of words in a file

    Args:
        filepath (str): The path to the file to count words in

    Returns:
        int: The number of words in the file
    """
    total_words = 0

    with open(filepath, "r") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            total_words += len(chunk.split())
    return total_words


def count_bytes(filepath: str) -> int:
    """Counts the number of bytes in a file

    Args:
        filepath (str): The path to the file to count bytes in

    Returns:
        int: The number of bytes in the file
    """
    total_bytes = 0
    # Read in binary mode
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            total_bytes += len(chunk)
    return total_bytes


def count_chars(filepath: str) -> int:
    """Counts the number of characters in a file

    Args:
        filepath (str): The path to the file to count characters in

    Returns:
        int: The number of characters in the file
    """
    # Count the number of characters, including newlines and whitespace
    total_chars = 0
    with open(filepath, "r") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            total_chars += len(chunk)
    return total_chars


def main() -> None:
    """
    The main function to emulate the wc command.
    """
    parser = argparse.ArgumentParser(
        description="A simple module which replicates the functionality of the Unix wc command."
    )
    parser.add_argument("files", default=None, nargs="*", help="The files to count")
    parser.add_argument("-l", "--lines", action="store_true", help="Count lines")
    parser.add_argument("-w", "--words", action="store_true", help="Count words")
    parser.add_argument("-c", "--bytes", action="store_true", help="Count bytes")
    parser.add_argument("-m", "--chars", action="store_true", help="Count characters")
    args = parser.parse_args()

    # Show all by default
    if not args.lines and not args.words and not args.bytes and not args.chars:
        args.lines = True
        args.words = True
        args.bytes = True
        args.chars = True

    if args.files:
        result_str = ""
        for filepath in args.files:
            if os.path.isfile(filepath):
                result_str += f"wc for {filepath}: \n"
                if args.lines:
                    result_str += f"Lines: {count_lines(filepath)} "
                if args.words:
                    result_str += f"Words: {count_words(filepath)} "
                if args.bytes:
                    result_str += f"Bytes: {count_bytes(filepath)} "
                if args.chars:
                    result_str += f"Characters: {count_chars(filepath)} "
            else:
                result_str += f"{filepath} is not a file. Please check the path."
            result_str += "\n"
    else:
        # Get input from stdin and write to a temporary file
        import tempfile

        # Create a temporary file to store stdin content
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            while True:
                chunk = sys.stdin.read(CHUNK_SIZE)
                if not chunk:
                    break
                temp_file.write(chunk)
        temp_path = temp_file.name

        result_str = "Standard input: "
        if args.lines:
            result_str += f"Lines: {count_lines(temp_path)} "
        if args.words:
            result_str += f"Words: {count_words(temp_path)} "
        if args.bytes:
            result_str += f"Bytes: {count_bytes(temp_path)} "
        if args.chars:
            result_str += f"Characters: {count_chars(temp_path)} "

    print(result_str)
    return result_str


if __name__ == "__main__":
    main()
