from string import Template

def get_lang_selector(current_lang: str = "en"):
    langs = {"en": "EN", "es": "ES", "fr": "FR"}
    links = []
    for code, label in langs.items():
        border = "2px solid #333" if code == current_lang else "1px solid #999"
        bg = "#333" if code == current_lang else "transparent"
        color = "#fff" if code == current_lang else "#333"
        links.append(f'<a href="/?lang={code}" data-track-click="lang_{code}" style="display: inline-block; padding: 5px 15px; border: {border}; border-radius: 4px; text-decoration: none; background: {bg}; color: {color};">{label}</a>')
    links_html = " ".join(links)
    return f"""<div style="padding: 0px 10vw; margin-top: 10px; display: flex; gap: 10px;">
    {links_html}
</div>
"""
