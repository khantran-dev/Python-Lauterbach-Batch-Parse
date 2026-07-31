import logging
import re
from pathlib import Path

from .models import DebugCable, License, LicenseCategory

logger = logging.getLogger(__name__)

# Matches: "; Feature upgrade file for DebugCable C08110115002"
_CABLE_HEADER_RE = re.compile(r"^;\s+Feature upgrade file for DebugCable\s+(\S+)", re.IGNORECASE)

# Matches: "; C08110115002 valid until vers. 09/2026  (Arm® / Cortex®)"
# Captures: serial, expiry, category name (inside parentheses)
_CATEGORY_RE = re.compile(
    r"^;\s+(\S+)\s+valid until vers\.\s+(\S+)\s+\((.+?)\)",
    re.IGNORECASE,
)

# Matches: ";   LA-7742  ARM9"  or  ";   LA-3743X ARMv8/v9-A/R"
_LICENSE_RE = re.compile(r"^;\s{3,}(\S+)\s+(.+)$")


class CmmParser:
    """Parses a single Lauterbach TRACE32 .cmm feature upgrade file."""

    def parse_file(self, path: Path) -> DebugCable | None:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            logger.error("Cannot read %s: %s", path, exc)
            return None

        return self._parse_text(text, source=str(path))

    def _parse_text(self, text: str, source: str = "<unknown>") -> DebugCable | None:
        lines = text.splitlines()

        cable_serial: str | None = None
        categories: list[LicenseCategory] = []
        current_category: LicenseCategory | None = None

        for lineno, raw in enumerate(lines, start=1):
            line = raw.rstrip()

            # ── Debug cable serial ─────────────────────────────────────────
            if cable_serial is None:
                m = _CABLE_HEADER_RE.match(line)
                if m:
                    cable_serial = m.group(1)
                    logger.debug("Line %d: cable serial %s", lineno, cable_serial)
                    continue

            # ── Category header ────────────────────────────────────────────
            m = _CATEGORY_RE.match(line)
            if m:
                if current_category is not None:
                    categories.append(current_category)
                cat_serial = m.group(1)
                cat_name = _normalize_category_name(m.group(3))
                current_category = LicenseCategory(serial=cat_serial, name=cat_name)
                logger.debug("Line %d: category %s (%s)", lineno, cat_name, cat_serial)
                continue

            # ── License entry ──────────────────────────────────────────────
            if current_category is not None:
                m = _LICENSE_RE.match(line)
                if m:
                    lic = License(code=m.group(1), name=m.group(2).strip())
                    current_category.licenses.append(lic)
                    logger.debug("Line %d: license %s %s", lineno, lic.code, lic.name)

        if current_category is not None:
            categories.append(current_category)

        if cable_serial is None:
            logger.warning("%s: no DebugCable serial found — file may be malformed", source)
            return None

        return DebugCable(serial=cable_serial, categories=categories)


def _normalize_category_name(raw: str) -> str:
    """Strip trademark symbols and normalise whitespace."""
    cleaned = re.sub(r"[®™]", "", raw)
    return " ".join(cleaned.split())
