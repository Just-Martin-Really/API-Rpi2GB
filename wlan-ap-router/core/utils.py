#  Low-level helpers: shell execution, file I/O, console output.
#  No business logic here – only reusable primitives.


import os
import shutil
import subprocess


def run(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Execute a shell command. Returns CompletedProcess."""
    return subprocess.run(
        cmd, shell=True, check=check,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )



def deploy_file(src: str, dest: str) -> None:
    """Copy src to dest. Creates a .bak backup if dest already exists."""
    if not os.path.exists(src):
        print_warn(f"Source file not found: {src}  – skipping")
        return
    if os.path.exists(dest):
        shutil.copy2(dest, dest + ".bak")
        print_info(f"Backup created: {dest}.bak")
    shutil.copy2(src, dest)
    print_ok(f"Deployed: {src}  →  {dest}")


def line_in_file(path: str, line: str) -> bool:
    """Return True if the exact line already exists in the file."""
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as f:
        return any(l.strip() == line.strip() for l in f)


def append_to_file(path: str, content: str) -> None:
    """Append content to a file."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)


def print_ok(msg: str) -> None:
    print(f"OK:   {msg}")

def print_info(msg: str) -> None:
    print(f"INFO: {msg}")

def print_warn(msg: str) -> None:
    print(f"WARN: {msg}")
