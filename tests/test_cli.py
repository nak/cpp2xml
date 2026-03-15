"""Tests for the CLI interface."""

import unittest
from pathlib import Path
import sys
import tempfile
import shutil

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cpp2xml.cli import parse_args, main


class TestCli(unittest.TestCase):
    """Test cases for CLI."""

    def setUp(self):
        """Set up test output directory."""
        self.output_dir = tempfile.mkdtemp()
        self.fixtures_dir = Path(__file__).parent / "fixtures" / "include"

    def tearDown(self):
        """Clean up test output directory."""
        shutil.rmtree(self.output_dir)

    def test_parse_args_basic(self):
        """Test basic argument parsing."""
        args = parse_args(["-I", "/usr/include", "-o", "/tmp/output"])
        self.assertEqual(args.include_paths, ["/usr/include"])
        self.assertEqual(args.output_dir, "/tmp/output")

    def test_parse_args_multiple_includes(self):
        """Test parsing multiple include paths."""
        args = parse_args([
            "-I", "/usr/include",
            "-I", "/usr/local/include",
            "-o", "/tmp/output"
        ])
        self.assertEqual(len(args.include_paths), 2)

    def test_parse_args_with_files(self):
        """Test parsing with specific files."""
        args = parse_args([
            "-I", "/usr/include",
            "-f", "header1.h",
            "-f", "header2.h",
            "-o", "/tmp/output"
        ])
        self.assertEqual(len(args.files), 2)

    def test_main_with_all_headers(self):
        """Test main function parsing all headers."""
        result = main([
            "-I", str(self.fixtures_dir),
            "-o", self.output_dir
        ])

        self.assertEqual(result, 0)

        # Check that XML files were created
        xml_files = list(Path(self.output_dir).rglob("*.xml"))
        self.assertGreater(len(xml_files), 0)

    def test_main_with_specific_file(self):
        """Test main function with specific file."""
        simple_header = self.fixtures_dir / "simple.h"
        result = main([
            "-I", str(self.fixtures_dir),
            "-f", str(simple_header),
            "-o", self.output_dir
        ])

        self.assertEqual(result, 0)

        output_file = Path(self.output_dir) / "simple.xml"
        self.assertTrue(output_file.exists())

    def test_main_with_invalid_include_path(self):
        """Test main function with invalid include path."""
        result = main([
            "-I", "/nonexistent/path",
            "-o", self.output_dir
        ])

        self.assertNotEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
