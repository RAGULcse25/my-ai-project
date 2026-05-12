import os

# ─────────────────────────────────────────
# FILE WRITER
# Creates folders and writes code to disk
# ─────────────────────────────────────────

def create_project_folder(project_name: str) -> str:
    """Creates output/project_name/ folder"""
    
    # Clean project name for folder
    folder_name = project_name.lower().replace(" ", "_")
    output_path = os.path.join("output", folder_name)
    
    os.makedirs(output_path, exist_ok=True)
    print(f"📁 Created folder: {output_path}")
    
    return output_path


def write_file(folder_path: str, filename: str, content: str):
    """Writes a single file to the project folder"""
    
    file_path = os.path.join(folder_path, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✅ Written: {filename} ({len(content)} chars)")
    return file_path


def write_all_files(folder_path: str, files: dict):
    """
    files = {
      "main.py": "...code...",
      "model.py": "...code...",
      ...
    }
    """
    written = []
    for filename, content in files.items():
        path = write_file(folder_path, filename, content)
        written.append(path)
    
    print(f"\n📦 Total files written: {len(written)}")
    return written
