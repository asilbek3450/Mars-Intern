"""
Root entrypoint for local and Railway deployments.
"""
import asyncio
import importlib.util
import sys
from pathlib import Path


SRC_DIR = Path(__file__).parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def load_app_main():
    """Load src/main.py without colliding with this file name."""
    module_path = SRC_DIR / "main.py"
    spec = importlib.util.spec_from_file_location("mars_intern_app_main", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load application entrypoint: {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.main


if __name__ == "__main__":
    try:
        asyncio.run(load_app_main()())
    except KeyboardInterrupt:
        print("\n❌ Bot stopped")
