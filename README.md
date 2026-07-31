
---

## Required Software

        ### Python

        Python 3.11 or newer is required.

        Verify Python is installed:

        ```powershell
        py --version
        ```

        Expected:

        ```text
        Python 3.11+
        ```

        If Python is not installed:

        1. Download Python from:
        https://www.python.org/downloads/

        2. During installation, make sure to check:

        ```text
        ✅ Add Python to PATH
        ```

        3. Verify installation:

        ```powershell
        py --version
        ```

# Initial Setup

Open PowerShell and navigate to the project folder:

1. Open the Folder:

```text
Python-Lauterbach-Batch-Parse
```

2. In File Explorer, click inside the folder

3. In the address bar, type:

```text
powershell
```

4. Press Enter

PowerShell will open directly in the project folder

Install required Python packages:

```powershell
py -m pip install -r requirements.txt
```

Expected:

```text
Successfully installed openpyxl
```

---

# Adding CMM Files

Place all Lauterbach `.cmm` files into:

```text
input_folder
```

---

# Running The Program

## Process All Files In Input Folder

```powershell
py main.py input_folder
```

---

## Generate A Custom Excel Filename

```powershell
py main.py input_folder --excel my_export.xlsx
```

---

# Output Folder Structure

Every execution creates a new timestamped output folder.

Example:

```text
outputs
│
├── 20260731_091100
│   ├── lauterbach_output_20260731_091100.xlsx
│   └── run_summary.txt
│
├── 20260731_101530
│   ├── lauterbach_output_20260731_101530.xlsx
│   └── run_summary.txt
│
└── 20260731_143215
    ├── lauterbach_output_20260731_143215.xlsx
    └── run_summary.txt
```

No previous outputs are overwritten.

---

# Troubleshooting


## Python Not Found

Verify:

```powershell
py --version
```

If Python is not found:

1. Reinstall Python
2. Make sure:

```text
✅ Add Python to PATH
```

is selected during installation

---

## No CMM Files Found

Verify files exist:

```powershell
ls input_folder
```

Verify file extensions:

```text
.cmm
```

---

## Excel File Not Generated

Check the outputs folder:

```powershell
ls outputs
```

Open outputs folder:

```powershell
explorer .\outputs\
```

Open the newest timestamped folder.

---

## Reinstall Dependencies

```powershell
py -m pip install -r requirements.txt --upgrade
```

---

# Typical Workflow

```powershell
# 1. Copy all .cmm files into input_folder

# 2. Run parser
py main.py input_folder

# 3. Open outputs folder
explorer .\outputs\

# 4. Open generated Excel file

# 5. Review data

# 6. Use spreadsheet for asset import workflows
```
