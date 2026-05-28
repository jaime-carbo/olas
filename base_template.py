from string import Template

def get_template():

    return Template(
"""
<!DOCTYPE html>
<html>
<head><style>html { height: 100%; } body { min-height: 100vh; overflow-y: auto; margin: 0; font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace; font-size: 1.2vw; } pre { font-family: inherit; font-size: inherit; }</style></head>
$header
$lang_selector
$bio
$cluster
</body>
</html>
""")

