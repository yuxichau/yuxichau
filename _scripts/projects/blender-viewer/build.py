#!/usr/bin/env python3
"""Copy the dependency-free viewer source into the site's static asset tree."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
source = ROOT / "source" / "index.html"
destination = ROOT.parents[2] / "assets" / "projects" / "blender-viewer" / "index.html"
destination.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, destination)
print(f"built {destination.relative_to(ROOT.parents[2])}")
