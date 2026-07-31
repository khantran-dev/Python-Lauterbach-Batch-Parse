import logging
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

from .models import DebugCable

logger = logging.getLogger(__name__)

# Header columns in exact required order.
# An empty string produces the intentional blank column between
# "QPI Shipped Date" and "Eng Group".
_HEADERS = [
    "Asset tag",
    "Serial number",
    "Serial Number(Secondary)",
    "QC MFG Serial Number",
    "PO Number",
    "Model",
    "State",
    "Substate",
    "Assigned to",
    "Department",
    "Location",
    "Stockroom",
    "Comments",
    "Received Date",
    "Key Contact",
    "Condition",
    "Station name",
    "station type",
    "ECID",
    "Axiom tech team",
    "Memory Upgrade",
    "MSM Upgrade",
    "PMIC Upgrade",
    "RF Upgrade",
    "Local Upgrade Register",
    "WCN Upgrade",
    "IMEI",
    "Cost Center",
    "Parent",
    "Tech team",
    "QPI Shipped Date",
    "",           # intentional blank column
    "Eng Group",
]

_COL_SERIAL = _HEADERS.index("Serial number") + 1
_COL_MODEL  = _HEADERS.index("Model") + 1
_COL_STATE  = _HEADERS.index("State") + 1
_COL_SUBSTATE = _HEADERS.index("Substate") + 1


class ExcelWriter:
    """Converts a list of DebugCable objects into an .xlsx file."""

    def write(self, cables: list[DebugCable], output_path: Path) -> bool:
        """Write *cables* to *output_path*.  Returns True on success."""
        wb = Workbook()
        ws = wb.active
        ws.title = "Serials"

        # Header row
        ws.append(_HEADERS)
        for cell in ws[1]:
            cell.font = Font(bold=True)

        for cable in cables:
            self._write_cable(ws, cable)

        try:
            wb.save(output_path)
            logger.debug("Excel saved to %s", output_path)
            return True
        except OSError as exc:
            logger.error("Failed to save Excel file %s: %s", output_path, exc)
            return False

    # ------------------------------------------------------------------

    def _write_cable(self, ws, cable: DebugCable) -> None:
        # One row for the DebugCable serial itself
        row = _empty_row()
        row[_COL_SERIAL - 1] = cable.serial
        row[_COL_STATE - 1]  = "In use"
        row[_COL_SUBSTATE - 1] = "Issued"
        ws.append(row)

        # One row per license category
        for category in cable.categories:
            row = _empty_row()
            row[_COL_SERIAL - 1]  = category.serial
            row[_COL_STATE - 1]   = "In use"
            row[_COL_SUBSTATE - 1] = "Issued"
            if category.licenses:
                first = category.licenses[0]
                row[_COL_MODEL - 1] = f"{first.code} {first.name}"
            ws.append(row)


def _empty_row() -> list:
    return [""] * len(_HEADERS)
