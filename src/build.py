"""
SAF Build Script
================
Injects app/data.js and logo base64 into app/template.html to generate
standalone index.html (standard entry point) and ally.html.
"""

import os
import sys
import base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(BASE_DIR, "app", "data.js")
TEMPLATE_HTML = os.path.join(BASE_DIR, "app", "template.html")
LOGO_PNG = os.path.join(BASE_DIR, "app", "logo.png")

# Standard entry points
DIST_INDEX = os.path.join(BASE_DIR, "dist", "index.html")
ROOT_INDEX = os.path.join(BASE_DIR, "index.html")

# Aliases for backwards compatibility
DIST_ALLY = os.path.join(BASE_DIR, "dist", "ally.html")
ROOT_ALLY = os.path.join(BASE_DIR, "ally.html")


def build():
    if not os.path.exists(DATA_JS):
        print(f"Error: {DATA_JS} not found. Run extract.py first.")
        sys.exit(1)
        
    if not os.path.exists(TEMPLATE_HTML):
        print(f"Error: {TEMPLATE_HTML} not found.")
        sys.exit(1)

    print("Reading data...")
    with open(DATA_JS, "r", encoding="utf-8") as f:
        data_content = f.read()

    print("Reading template...")
    with open(TEMPLATE_HTML, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Logo base64 conversion
    logo_data_uri = "https://mcmegufmg.github.io/website/assets/img/logo.png"
    if os.path.exists(LOGO_PNG):
        try:
            with open(LOGO_PNG, "rb") as lf:
                b64_str = base64.b64encode(lf.read()).decode("utf-8")
                logo_data_uri = f"data:image/png;base64,{b64_str}"
                print("Inlined logo.png as base64 data URI.")
        except Exception as e:
            print(f"Warning: Could not read logo.png ({e}), using remote fallback.")

    print("Injecting database into template...")
    final_html = template_content.replace("/* DATA_PLACEHOLDER */", data_content)

    os.makedirs(os.path.dirname(DIST_INDEX), exist_ok=True)
    
    # Save standard index.html
    with open(DIST_INDEX, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"[Success] Built standard app: {DIST_INDEX}")

    with open(ROOT_INDEX, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"[Success] Updated root index: {ROOT_INDEX}")

    # Also keep ally.html aliases
    with open(DIST_ALLY, "w", encoding="utf-8") as f:
        f.write(final_html)
    with open(ROOT_ALLY, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"[Success] Updated ally.html aliases for compatibility.")


if __name__ == "__main__":
    build()
