from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("AI Sticky notes")
NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")

def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")

@mcp.tool()
def add_note(message: str) -> str:
    """
    Append a new node to a sticky note file

    Args:
        message (str): the note content to be added

    Returns:
        str: Confirmation message indicating the adding of the content
    """
    ensure_file()
    with open(NOTES_FILE, "a") as f:
        f.write(message + "\n")
    return "Note saved!"

@mcp.tool()
def read_notes() -> str:
    """
    Read and return all notes from the sticky note file.

    Returns:
        str: All notes as a single string separated by line breaks.
             If no notes exist, a default message is returned.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
    return content or "No notes yet"

def main():
    """Entry point for the direct execution server."""
    mcp.run()

if __name__ == "__main__":

    main()
