"""Genera badges/coverage.svg y badges/mutation.svg a partir de los reportes
que produce el workflow de CI: coverage.xml (pytest-cov) y mutmut.xml
(el junitxml que exporta mutmut).

El score de mutación cuenta los mutantes "timeout" como matados, igual que
el propio mutmut (ver la leyenda de `mutmut run`: un mutante que hace que
los tests tarden 10x más también se considera atrapado).
"""

import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

BADGES_DIR = Path("badges")
THRESHOLDS = ["50=red", "70=orange", "90=green"]


def coverage_percentage(coverage_xml: Path) -> float:
    root = ET.parse(coverage_xml).getroot()
    return round(float(root.attrib["line-rate"]) * 100, 1)


def mutation_percentage(mutmut_junitxml: Path) -> float:
    root = ET.parse(mutmut_junitxml).getroot()
    total = int(root.attrib["tests"])
    survived = int(root.attrib["failures"])
    skipped = int(root.attrib.get("skipped", 0))

    scored = total - skipped
    if scored == 0:
        return 0.0

    killed_or_timed_out = scored - survived
    return round(killed_or_timed_out / scored * 100, 1)


def make_badge(label: str, value: float, output: Path) -> None:
    BADGES_DIR.mkdir(exist_ok=True)
    subprocess.run(
        [
            sys.executable, "-m", "anybadge",
            "--overwrite",
            f"--label={label}",
            f"--value={value}",
            "--suffix=%",
            f"--file={output}",
            *THRESHOLDS,
        ],
        check=True,
    )


if __name__ == "__main__":
    coverage = coverage_percentage(Path("coverage.xml"))
    mutation = mutation_percentage(Path("mutmut.xml"))

    make_badge("coverage", coverage, BADGES_DIR / "coverage.svg")
    make_badge("mutation score", mutation, BADGES_DIR / "mutation.svg")

    print(f"coverage: {coverage}%")
    print(f"mutation score: {mutation}%")
