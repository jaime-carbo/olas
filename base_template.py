from string import Template

def get_template():

    return Template(
"""
<!DOCTYPE html>
<html>
$header
$lang_selector
$bio
</body>
</html>
""")

