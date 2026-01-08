#!/usr/bin/env python3
"""
Hernoem alle bestanden in OpenBooks naar zero-padded formaat.

Ondersteunt patronen zoals:
- 1_1.jpg -> 1_001.jpg
- GBV 1950-1.png -> GBV 1950-001.png
- VB 1974-1.png -> VB 1974-001.png
"""

import os
import re
from pathlib import Path

OPENBOOKS_DIR = Path("/home/maarten/Documents/GitHub/OpenBooks")

# Patronen voor verschillende bestandsnamen
PATTERNS = [
    # Patroon: prefix_nummer.ext (bijv. 1_1.jpg, 0_inhoudsopgave.jpg)
    (r"^(\d+)_(\d+)\.(\w+)$", lambda m: f"{m.group(1)}_{int(m.group(2)):03d}.{m.group(3)}"),

    # Patroon: Naam JAAR-nummer.ext (bijv. GBV 1950-1.png, VB 1974-10.png)
    (r"^(.+\s\d{4})-(\d+)\.(\w+)$", lambda m: f"{m.group(1)}-{int(m.group(2)):03d}.{m.group(3)}"),

    # Patroon: Naam-nummer.ext (bijv. something-1.png)
    (r"^(.+)-(\d+)\.(\w+)$", lambda m: f"{m.group(1)}-{int(m.group(2)):03d}.{m.group(3)}"),
]

def needs_padding(filename: str) -> bool:
    """Check of bestandsnaam padding nodig heeft (nummer < 100 zonder voorloopnullen)."""
    for pattern, _ in PATTERNS:
        match = re.match(pattern, filename)
        if match:
            # Vind de nummer-groep (meestal groep 2)
            groups = match.groups()
            for g in groups:
                if g and g.isdigit() and len(g) < 3 and int(g) < 100:
                    return True
    return False

def get_new_name(filename: str) -> str | None:
    """Bepaal nieuwe bestandsnaam met zero-padding."""
    for pattern, formatter in PATTERNS:
        match = re.match(pattern, filename)
        if match:
            new_name = formatter(match)
            if new_name != filename:
                return new_name
    return None

def process_folder(folder: Path) -> int:
    """Verwerk alle bestanden in een map."""
    renamed = 0

    for f in folder.iterdir():
        if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.tif', '.tiff']:
            new_name = get_new_name(f.name)
            if new_name:
                new_path = f.parent / new_name
                if not new_path.exists():
                    f.rename(new_path)
                    print(f"  {f.name} -> {new_name}")
                    renamed += 1
                else:
                    print(f"  SKIP (bestaat al): {new_name}")

    return renamed

def main():
    total_renamed = 0

    print("=" * 60)
    print("OpenBooks - Rename All Files to Zero-Padded Format")
    print("=" * 60)
    print()

    # Vind alle submappen (boeken)
    for item in sorted(OPENBOOKS_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            print(f"\n📚 {item.name}")
            print("-" * 50)

            renamed = process_folder(item)
            total_renamed += renamed

            if renamed == 0:
                print("  (geen bestanden om te hernoemen)")

    print()
    print("=" * 60)
    print(f"✅ Klaar! Totaal {total_renamed} bestanden hernoemd.")
    print("=" * 60)

if __name__ == "__main__":
    main()
