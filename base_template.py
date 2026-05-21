from string import Template

def get_template():

    return Template(
"""
<!DOCTYPE html>
<html>
$header
$bio
</body>
</html>
""")

