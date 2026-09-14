#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
source = ROOT / "_scripts/projects/blender-viewer/source/index.html"
artifact = ROOT / "assets/projects/blender-viewer/index.html"
for path in (source, artifact):
    text = path.read_text()
    assert '<canvas id="scene"' in text, f"missing canvas in {path}"
    assert 'FileReader' in text and 'parseObj' in text, f"missing OBJ loader in {path}"
    assert 'src="http' not in text, f"external dependency in {path}"
    scripts = re.findall(r'<script>(.*?)</script>', text, flags=re.S)
    assert scripts, f"missing inline script in {path}"
print(f"checked source and artifact: {source.relative_to(ROOT)}, {artifact.relative_to(ROOT)}")
print("dependency check: no external script URLs")
