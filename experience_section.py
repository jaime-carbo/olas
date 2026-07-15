from body_texts import get_text_by_name
from ascii_chart import create_tech_grid


def _parse_tech_file(text):
    entries = []
    current = None
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            if current:
                entries.append(current)
                current = None
            continue
        if line.startswith("[") and line.endswith("]"):
            if current:
                entries.append(current)
            parts = line[1:-1].split(" @ ", 1)
            current = {"role": parts[0], "company": parts[1] if len(parts) > 1 else "", "date": "", "techs": []}
        elif current is not None:
            if not current["date"] and ":" not in line:
                current["date"] = line
            elif ":" in line:
                cat, techs = line.split(":", 1)
                current["techs"].append((cat.strip(), techs.strip()))
    if current:
        entries.append(current)
    return entries


def get_experience_section(language: str = "en"):
    text = get_text_by_name("experience_par", language)
    tech_text = get_text_by_name("experience_tech", language)
    entries = _parse_tech_file(tech_text)
    grid = create_tech_grid(entries, width=80, title="EXPERIENCE")

    return f"""<div data-track="experience">
<div style="padding: 0px 10vw; margin-top: 20px; display: flex; border-radius: 5px;">
    <div style="flex: 1; padding: 10px;">
        <p>{text}</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 1; padding: 10px; display: flex; flex-direction: column; justify-content: center;">
        <pre style="margin: 0; font-size: 0.8vw;">{grid}</pre>
    </div>
</div>
</div>"""
