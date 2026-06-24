from string import Template
from body_texts import get_text_by_name

def get_mongodb_section(language: str = "en"):
    text = get_text_by_name("mongodb_par", language)
    return Template("""
<div data-track="mongodb">
<div style="padding: 0px 10vw; margin-top: 20px; display: flex; border-radius: 5px;">
    <div style="flex: 7; padding: 10px;">
        <p>$text</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 3; padding: 10px; display: flex; flex-direction: column; justify-content: center;">
        <pre id="mongoLangChart" style="margin: 0; font-size: 0.8vw;">LANG │ loading...</pre>
        <pre id="mongoSectionsChart" style="margin: 0; margin-top: 15px; font-size: 0.8vw;">SECT │ loading...</pre>
    </div>
</div>
<script>
    function measureMongoChar() {
        const ctx = document.createElement('canvas').getContext('2d');
        ctx.font = getComputedStyle(document.getElementById("mongoLangChart")).font;
        const metrics = ctx.measureText('M');
        const charWidth = metrics.width;
        const charHeight = (metrics.fontBoundingBoxAscent + metrics.fontBoundingBoxDescent) * 3;
        return { charWidth, charHeight };
    }
    function connectMongoLang() {
        const { charWidth, charHeight } = measureMongoChar();
        const container = document.getElementById("mongoLangChart").parentElement;
        const width = container.clientWidth;
        langEs = new EventSource(`/mongoLangChart?width=$${width}&height=$${charHeight * 5}&charWidth=$${charWidth}&charHeight=$${charHeight}`);
        langEs.addEventListener('message', (e) => {
            document.getElementById("mongoLangChart").textContent = e.data;
        });
        langEs.addEventListener('error', () => {
            document.getElementById("mongoLangChart").textContent = "LANG │ offline";
            langEs.close();
        });
    }
    function connectMongoSections() {
        const { charWidth, charHeight } = measureMongoChar();
        const container = document.getElementById("mongoSectionsChart").parentElement;
        const width = container.clientWidth;
        sectionsEs = new EventSource(`/mongoSectionsChart?width=$${width}&height=$${charHeight * 5}&charWidth=$${charWidth}&charHeight=$${charHeight}&lang=$language`);
        sectionsEs.addEventListener('message', (e) => {
            document.getElementById("mongoSectionsChart").textContent = e.data;
        });
        sectionsEs.addEventListener('error', () => {
            document.getElementById("mongoSectionsChart").textContent = "SECT │ offline";
            sectionsEs.close();
        });
    }
    connectMongoLang();
    connectMongoSections();
</script>
</div>
""").substitute(text=text, language=language)
