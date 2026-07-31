"""
Python-Lauterbach-Batch-Parse
Entry point:
  python main.py sample.cmm                          # single file
  python main.py input_folder                        # folder, timestamped output
  python main.py input_folder --excel custom.xlsx    # folder, custom output name
"""
import argparse
import datetime
import logging
import sys
from pathlib import Path

from src import CmmParser, ExcelWriter, TerminalFormatter
from src.models import DebugCable

_DIVIDER = "=" * 50
_OUTPUTS_ROOT = Path("outputs")
_LABEL_WIDTH = 19


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="main",
        description="Parse Lauterbach TRACE32 .cmm feature upgrade files.",
    )
    p.add_argument(
        "input",
        type=Path,
        help="Path to a single .cmm file or a folder containing .cmm files",
    )
    p.add_argument(
        "--excel",
        type=Path,
        default=None,
        metavar="FILE",
        help="Excel output file name (default: lauterbach_output_YYYYMMDD_HHMMSS.xlsx)",
    )
    p.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    return p


def _collect_paths(input_path: Path) -> list[Path]:
    """Return sorted list of .cmm paths from a file or folder."""
    if input_path.is_file():
        return [input_path]
    return sorted(input_path.glob("*.cmm"))


def _process_files(
    paths: list[Path], parser: CmmParser, formatter: TerminalFormatter
) -> tuple[list[DebugCable], int]:
    """Parse and print each file.  Returns (cables, failed_count)."""
    cables: list[DebugCable] = []
    failed = 0

    for path in paths:
        print(f"\n{_DIVIDER}")
        print(f"File: {path.name}")
        print(_DIVIDER)

        cable = parser.parse_file(path)
        if cable is None:
            print(f"  Warning: could not parse {path.name}", file=sys.stderr)
            failed += 1
            continue

        formatter.print(cable)
        cables.append(cable)

    return cables, failed


def _write_run_summary(
    out_dir: Path,
    timestamp: str,
    found: int,
    processed: int,
    failed: int,
    excel_name: str,
) -> None:
    content = (
        f"Run Timestamp: {timestamp}\n"
        f"\n"
        f"Files Found: {found}\n"
        f"Files Processed: {processed}\n"
        f"Files Failed: {failed}\n"
        f"\n"
        f"Excel Output:\n"
        f"{excel_name}\n"
    )
    (out_dir / "run_summary.txt").write_text(content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    input_path: Path = args.input

    if not input_path.exists():
        print(f"Error: path not found: {input_path}", file=sys.stderr)
        return 1

    paths = _collect_paths(input_path)

    if not paths:
        print(f"Error: no .cmm files found in {input_path}", file=sys.stderr)
        return 1

    # Create timestamped output folder
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = _OUTPUTS_ROOT / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)

    # Resolve Excel path: user-supplied name goes into the output folder as-is
    excel_name = args.excel.name if args.excel else f"lauterbach_output_{timestamp}.xlsx"
    excel_path = out_dir / excel_name

    parser = CmmParser()
    formatter = TerminalFormatter()

    cables, failed = _process_files(paths, parser, formatter)

    # Write Excel
    excel_ok = True
    if cables:
        excel_ok = ExcelWriter().write(cables, excel_path)
        if not excel_ok:
            print(f"Error: failed to write Excel file: {excel_path}", file=sys.stderr)

    # Write run_summary.txt
    _write_run_summary(out_dir, timestamp, len(paths), len(cables), failed, excel_name)

    # Batch summary
    W = _LABEL_WIDTH
    print(f"\n{_DIVIDER}")
    print("Batch Summary")
    print(_DIVIDER)
    print(f"\n{'Files Found:':<{W}}{len(paths)}")
    print(f"{'Files Processed:':<{W}}{len(cables)}")
    print(f"{'Files Failed:':<{W}}{failed}")
    print(f"\nOutput Folder:")
    print(f"{out_dir}")
    if cables:
        print(f"\nExcel Output:")
        print(f"{excel_path}")

    return 0 if (failed == 0 and excel_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
