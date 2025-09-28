import json
from datetime import datetime
from pathlib import Path

# BASE_DIR is the directory containing this file (e.g. src/)
BASE_DIR = Path(__file__).resolve().parent

# REPO_ROOT is the parent of BASE_DIR's parent (two levels up)
REPO_ROOT = BASE_DIR.parent.parent

# NOTES_FILE inside the repo
NOTES_FILE = REPO_ROOT / "data" / "notes" / "notes.json"


def _load_notes() -> list:
    """Load notes from NOTES_FILE. Create file if it doesn't exist."""
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not NOTES_FILE.exists():
        NOTES_FILE.write_text("[]", encoding="utf-8")
        return []

    try:
        return json.loads(NOTES_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # If file is corrupted, reset to empty
        NOTES_FILE.write_text("[]", encoding="utf-8")
        return []


def _save_notes(notes: list) -> None:
    """Save notes to NOTES_FILE with pretty formatting."""
    NOTES_FILE.write_text(json.dumps(notes, indent=2), encoding="utf-8")


def add_note(text: str) -> dict:
    """Add a note and persist it."""
    notes = _load_notes()
    note = {
        "id": len(notes) + 1,
        "text": text,
        "created_at": datetime.now().isoformat(),
    }
    notes.append(note)
    _save_notes(notes)
    return note


def list_notes() -> list:
    """Return all notes."""
    return _load_notes()


def search_notes(query: str) -> list:
    """Search for notes containing the query string (case-insensitive)."""
    notes = _load_notes()
    return [n for n in notes if query.lower() in n["text"].lower()]


def delete_note(note_id: int) -> bool:
    """Delete a note by its ID. Returns True if deleted, False if not found."""
    notes = _load_notes()
    new_notes = [n for n in notes if n["id"] != note_id]
    if len(new_notes) == len(notes):
        return False  # not found
    _save_notes(new_notes)
    return True
