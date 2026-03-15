"""Command-line interface for cpp2xml."""

import argparse
import sys
from pathlib import Path

from .parser import CppParser
from .xml_generator import XmlGenerator


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Parse C++ header files and generate XML documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse headers in a single include directory to package mylib
  cpp2xml -I /usr/include/mylib:mylib -o ./xml_output

  # Parse headers with multiple include paths to pkgs main_os and local_os
  cpp2xml -I /usr/include:main_os -I /usr/local/include:local_os -o ./xml_output

  # Pass additional clang arguments
  cpp2xml -I ./include:mylib -o ./xml_output -- -std=c++20 -DDEBUG
        """
    )

    parser.add_argument(
        "-I", "--include-path",
        action="append",
        dest="include_paths",
        metavar="PATH",
        required=True,
        help="Include directory to search for headers (can be specified multiple times)"
    )

    parser.add_argument(
        "-o", "--output-dir",
        required=True,
        metavar="DIR",
        help="Output directory for XML files"
    )

    parser.add_argument(
        "--clang-args",
        nargs="*",
        help="Additional arguments to pass to clang (use after --)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    return parser.parse_args(args)


def main(argv: list[str] | None = None):
    """Main entry point for the CLI."""
    if argv is None:
        argv = sys.argv[1:]

    # Handle -- separator for clang args
    if "--" in argv:
        separator_idx = argv.index("--")
        main_args = argv[:separator_idx]
        clang_args = argv[separator_idx + 1:]
    else:
        main_args = argv
        clang_args = []
    args = parse_args(main_args)
    include_path_mapping: dict[str, str] = {}
    # Validate include paths
    for include_path in args.include_paths:
        if ":" not in include_path:
            print(f"Invalid include path format: {include_path}. Expected format: 'path:module'"
                  " where 'module' specified the name of the python package name to generate for"
                  " the given include path")
            return 1
        true_path, target_module = include_path.split(":", 1)
        if not Path(include_path).exists():
            print(f"Error: Include path does not exist: {include_path}", file=sys.stderr)
            return 1
        include_path_mapping[include_path] = target_module

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.verbose:
        print(f"Include paths: {include_path_mapping}")
        print(f"Output directory: {output_dir}")
        if clang_args:
            print(f"Clang arguments: {clang_args}")

    # Initialize parser and generator
    parser = CppParser(
        include_paths=include_path_mapping,
        clang_args=clang_args
    )
    generator = XmlGenerator(output_dir=str(output_dir))

    try:
        # Parse all headers in include paths
        if args.verbose:
            print("Parsing all headers in include paths...")
        parsed_headers = parser.parse_all_headers()
        if args.verbose:
            print(f"Found {len(parsed_headers)} header file(s)")
        generator.generate_all(parsed_headers)
        print(f"\nSuccessfully generated XML files in: {output_dir}")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
