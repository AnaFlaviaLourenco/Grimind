import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Checkbox border-radius in CSS
# I'll replace border-radius: 50% with border-radius: 6px in `.chk` CSS
content = re.sub(r'(\.chk\{[^}]*border-radius:)var\(--radius-pill\)([^}]*\})', r'\g<1>6px\g<2>', content)
# It was var(--radius-pill) in the CSS! Wait, let me check the CSS for .chk using grep.
