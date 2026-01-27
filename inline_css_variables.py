"""
Script to inline all CSS variables in theme files.
Textual CSS doesn't support SCSS-style variables, so we need to replace them with actual values.
"""
import re
import sys
import io
from pathlib import Path

# Fix encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inline_variables(css_content):
    """Replace all $variable references with their defined values."""
    # Extract all variable definitions
    variables = {}
    var_pattern = r'\$([a-z0-9-]+):\s*([^;]+);'

    for match in re.finditer(var_pattern, css_content):
        var_name = match.group(1)
        var_value = match.group(2).strip()
        variables[var_name] = var_value

    # Remove variable definitions from CSS
    result = re.sub(r'/\*.*?\*/|^\s*\$[a-z0-9-]+:.*;$', '', css_content, flags=re.MULTILINE | re.DOTALL)

    # Replace all variable uses with their values
    for var_name, var_value in variables.items():
        result = result.replace(f'${var_name}', var_value)

    # Clean up empty lines
    result = re.sub(r'\n\s*\n\s*\n', '\n\n', result)

    return result

# Process all theme files
themes_dir = Path('themes')
for theme_file in themes_dir.glob('*.tcss'):
    print(f"Processing {theme_file.name}...")

    with open(theme_file, 'r', encoding='utf-8') as f:
        content = f.read()

    inlined = inline_variables(content)

    with open(theme_file, 'w', encoding='utf-8') as f:
        f.write(inlined)

    print(f"  [OK] Done")

print("\nAll theme files processed!")
