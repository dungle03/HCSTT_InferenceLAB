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


def main():
    """Run the web application."""
    app = create_app()
    print("=" * 60)
    print("🧠 Intelligent Diagnosis System")
    print("=" * 60)
    print("✅ Inference Lab: http://127.0.0.1:5000/lab")
    print("✅ Medical Diagnosis: http://127.0.0.1:5000/medical")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()
