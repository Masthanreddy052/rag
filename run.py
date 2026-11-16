
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run_command(command):
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)

if __name__ == "__main__":

    print("\n=== Step 1: Building Knowledge Base ===")
    run_command([sys.executable, "ingest.py"])

    print("\n=== Step 2: Starting Streamlit ===")
    run_command([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app.py"
    ])
