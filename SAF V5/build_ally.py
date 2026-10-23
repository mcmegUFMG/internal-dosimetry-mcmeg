import json

# Read data
with open(r'd:\SAF\data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

# Read template
with open(r'd:\SAF\template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Inject
final_html = html.replace('/* DATA_PLACEHOLDER */', data_js)

# Save
with open(r'd:\SAF\ally.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Created ally.html successfully!")
