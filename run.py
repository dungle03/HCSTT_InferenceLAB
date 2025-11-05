"""Main entry point for the Intelligent Diagnosis System.

Usage:
    python run.py
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from web import create_app
import socket


def _choose_port(candidates=(5000, 5001, 5050, 8080)) -> int:
    """Pick the first port we can bind to (workaround for Windows 10013)."""
    for p in candidates:
        s = socket.socket()
        try:
            s.bind(("127.0.0.1", p))
            s.close()
            return p
        except OSError:
            try:
                s.close()
            except Exception:
                pass
            continue
    # Fallback to last candidate if all quick probes failed
    return candidates[-1]


def main():
    """Run the web application."""
    app = create_app()
    print("=" * 60)
    print("🧠 Intelligent Diagnosis System")
    print("=" * 60)
    port = _choose_port()
    print(f"✅ Inference Lab: http://127.0.0.1:{port}/lab")
    print(f"✅ Sinusitis Diagnosis: http://127.0.0.1:{port}/sinusitis")
    print("=" * 60)
    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    main()
