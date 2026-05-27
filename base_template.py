from string import Template

def get_template():

    return Template(
"""
<!DOCTYPE html>
<html>
<head><style>html { height: 100%; } body { min-height: 100vh; overflow-y: auto; margin: 0; }</style></head>
$header
$lang_selector
$bio
$cluster
</body>
</html>
""")

