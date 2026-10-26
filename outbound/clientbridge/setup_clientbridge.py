"""Put the ClientBridge configuration in place for Harvey.

    python clientbridge/setup_clientbridge.py           # copy what's missing
    python clientbridge/setup_clientbridge.py --force   # overwrite with the templates

Copies harvey.local.yaml.example to harvey.local.yaml (gitignored, and it
wins over harvey.yaml), and the product knowledge and competitive intel into
skills/, where the writer and reply handler read them. Never overwrites your
edits unless you pass --force. Then checks the config loads and lists what
you still have to fill in.
"""

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COPIES = [
    (HERE / "harvey.local.yaml.example", ROOT / "harvey.local.yaml"),
    (HERE / "product_knowledge.md", ROOT / "skills" / "product_knowledge.md"),
    (HERE / "competitive_intel.md", ROOT / "skills" / "competitive_intel.md"),
]


def main() -> int:
    force = "--force" in sys.argv[1:]
    for src, dst in COPIES:
        if dst.exists() and not force:
            print(f"  kept     {dst.relative_to(ROOT)} (already there; --force replaces it)")
            continue
        shutil.copyfile(src, dst)
        print(f"  wrote    {dst.relative_to(ROOT)}")

    sys.path.insert(0, str(ROOT))
    from harvey.config import ConfigError, load_config

    local = ROOT / "harvey.local.yaml"
    try:
        load_config(str(local))
    except ConfigError as e:
        print(f"\nharvey.local.yaml doesn't load yet:\n  {e}")
        return 1
    todo = [line.strip() for line in local.read_text(encoding="utf-8").splitlines()
            if "CHANGE_ME" in line and not line.lstrip().startswith("#")]
    if todo:
        print("\nStill to fill in, in harvey.local.yaml:")
        for line in todo:
            print(f"  - {line}")
    else:
        print("\nharvey.local.yaml is complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
