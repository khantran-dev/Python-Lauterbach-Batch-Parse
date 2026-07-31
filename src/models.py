from dataclasses import dataclass, field


@dataclass
class License:
    code: str
    name: str


@dataclass
class LicenseCategory:
    serial: str
    name: str
    licenses: list[License] = field(default_factory=list)


@dataclass
class DebugCable:
    serial: str
    categories: list[LicenseCategory] = field(default_factory=list)
