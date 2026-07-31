# Python-Lauterbach-Batch-Parse

Command-line tool that parses Lauterbach TRACE32 `.cmm` feature upgrade files, prints license information to the terminal, and exports an Excel summary.

## Requirements

- Python 3.11+
- `openpyxl` (install via `pip install -r requirements.txt`)

## Usage

**Single file:**
```
python main.py sample.cmm
```

**Folder (processes all `.cmm` files, sorted):**
```
python main.py input_folder
```

**Folder with custom Excel output name:**
```
python main.py input_folder --excel my_export.xlsx
```

**Verbose debug logging:**
```
python main.py input_folder -v
```

## Output structure

Every run creates a unique timestamped folder under `outputs/`:

```
outputs/
└── YYYYMMDD_HHMMSS/
    ├── lauterbach_output_YYYYMMDD_HHMMSS.xlsx
    └── run_summary.txt
```

When `--excel my_export.xlsx` is supplied the Excel file is named `my_export.xlsx` but still placed inside the timestamped folder.

## Terminal output

Parsed cable data is printed for each file, followed by a batch summary:

```
==================================================
File: sample.cmm
==================================================
==================================================
Debug Cable
==================================================

Serial Number: C08110115002

==================================================
License Categories
==================================================

[Arm / Cortex]
Category Serial: C08110115002

  LA-7742   ARM9
  LA-7843X  ARMv7-A/R
  ...

==================================================
Batch Summary
==================================================

Files Found:       1
Files Processed:   1
Files Failed:      0

Output Folder:
outputs/20260731_090501

Excel Output:
outputs/20260731_090501/lauterbach_output_20260731_090501.xlsx
```

## run_summary.txt

A plain-text summary is written alongside the Excel file:

```
Run Timestamp: 20260731_090501

Files Found: 1
Files Processed: 1
Files Failed: 0

Excel Output:
lauterbach_output_20260731_090501.xlsx
```

## Excel output

The generated `.xlsx` file contains one row per serial number found across all processed files:

| Row type | Serial number | Model |
|---|---|---|
| DebugCable | cable serial | *(empty)* |
| License category | category serial | first license code + name |

`State` is set to `In use` and `Substate` to `Issued` for every row. All other columns are empty.

## Project structure

```
Python-Lauterbach-Batch-Parse/
│
├── main.py              # CLI entry point
├── requirements.txt
├── sample.cmm           # example input file
├── input_folder/        # place .cmm files here for batch processing
│
├── outputs/             # auto-created; one subfolder per run
│   └── YYYYMMDD_HHMMSS/
│       ├── lauterbach_output_YYYYMMDD_HHMMSS.xlsx
│       └── run_summary.txt
│
└── src/
    ├── __init__.py
    ├── models.py        # DebugCable, LicenseCategory, License dataclasses
    ├── parser.py        # CmmParser — reads .cmm files into model objects
    ├── formatter.py     # TerminalFormatter — renders to terminal
    └── excel_writer.py  # ExcelWriter — writes .xlsx
```
