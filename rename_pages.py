#!/usr/bin/env python3
"""Hernoem bestanden van 1_1.jpg naar 1_001.jpg formaat."""

import os
import re
from pathlib import Path

folder = Path("/home/maarten/Documents/GitHub/OpenBooks/Prof. D. Vandepitte Berekening van Constructies Boekdeel I")

renamed = 0
for f in folder.glob("*.jpg"):
    match = re.match(r"^(\d+)_(\d+)\.jpg$", f.name)
    if match:
        deel = match.group(1)
        pagina = int(match.group(2))
        new_name = f"{deel}_{pagina:03d}.jpg"

        if f.name != new_name:
            new_path = f.parent / new_name
            f.rename(new_path)
            print(f"{f.name} -> {new_name}")
            renamed += 1

print(f"\nKlaar! {renamed} bestanden hernoemd.")
