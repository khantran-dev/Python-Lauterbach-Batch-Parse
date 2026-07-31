from .models import DebugCable, LicenseCategory

_DIVIDER = "=" * 50


class TerminalFormatter:
    """Renders a DebugCable to human-readable terminal output."""

    def format(self, cable: DebugCable) -> str:
        lines: list[str] = []

        lines += [
            _DIVIDER,
            "Debug Cable",
            _DIVIDER,
            "",
            f"Serial Number: {cable.serial}",
            "",
        ]

        lines += [
            _DIVIDER,
            "License Categories",
            _DIVIDER,
        ]

        if not cable.categories:
            lines.append("\n  (no license categories found)")
        else:
            for category in cable.categories:
                lines.append("")
                lines += _format_category(category)

        return "\n".join(lines)

    def print(self, cable: DebugCable) -> None:
        print(self.format(cable))


def _format_category(category: LicenseCategory) -> list[str]:
    lines = [
        f"[{category.name}]",
        f"Category Serial: {category.serial}",
        "",
    ]

    if not category.licenses:
        lines.append("  (no licenses)")
        return lines

    # Align license names by padding the code column.
    max_code_len = max(len(lic.code) for lic in category.licenses)
    for lic in category.licenses:
        lines.append(f"  {lic.code:<{max_code_len}}  {lic.name}")

    return lines
