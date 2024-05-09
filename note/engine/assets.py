from pathlib import Path

assets = Path(__file__).resolve().parent / "assets"

assert assets.exists(), "assets directory note found"

notecss = assets / "note.css"
notejs = assets / "note.js"
