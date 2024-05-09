from pathlib import Path

assets = Path(__file__).resolve().parent / "assets"

assert assets.exists(), "assets directory note found"

notecss = assets / "notecss/note.css"
notejs = assets / "notejs/note.js"