"""
Tests for the ccwc module.
"""

import sys
import tempfile
from unittest.mock import patch

import pytest
from src.ccwc import (
    count_bytes,
    count_chars,
    count_lines,
    count_words,
    main,
)


def test_wc_functions():
    """
    Test individual counting functions
    """
    # Sample text for testing
    test_text = (
        "This is a sample text file.\nIt contains multiple lines,\nand several words.\n"
    )

    # Write temp test file
    # Create a temporary file to store stdin content
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write(test_text)
        temp_file.flush()
        temp_path = temp_file.name

    # Test individual counting functions
    assert count_lines(temp_path) == 3
    assert count_words(temp_path) == 13
    assert count_bytes(temp_path) == len(test_text.encode("utf-8"))
    assert count_chars(temp_path) == len(test_text)


@pytest.mark.parametrize(
    "args,expected_output",
    [
        (
            ["-l", "/Users/srimanth/Documents/Projects/CC_BYO/assets/test_wc.txt"],
            "Lines: 7145",
        ),
        (
            ["-w", "/Users/srimanth/Documents/Projects/CC_BYO/assets/test_wc.txt"],
            "Words: 58164",
        ),
        (
            ["-b", "/Users/srimanth/Documents/Projects/CC_BYO/assets/test_wc.txt"],
            "Bytes: 342190",
        ),
        (
            ["-c", "/Users/srimanth/Documents/Projects/CC_BYO/assets/test_wc.txt"],
            "Characters: 332147",
        ),
    ],
)
def test_main_with_args(args, expected_output):
    """
    Test main function with arguments, listed above

    Args:
        args (list): List of arguments to pass to main
        expected_output (str): Expected output from main
    """
    with patch.object(sys, "argv", ["ccwc.py"] + args):
        assert expected_output in main()


def test_main_without_args():
    """
    Test main function with no arguments
    """
    test_text = (
        "This is a sample text file.\nIt contains multiple lines,\nand several words.\n"
    )
    expected = (
        f"Lines: 3 Words: 13 Bytes: {len(test_text.encode('utf-8'))} "
        f"Characters: {len(test_text)} \n"
    )

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write(test_text)
        temp_file.flush()
        temp_path = temp_file.name

    with patch.object(sys, "argv", ["ccwc.py", temp_path]):
        assert expected in main()
