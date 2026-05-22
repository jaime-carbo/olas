from string import Template
from body_texts import get_text_by_name

def get_bio(language: str = "en"):
    return Template(
    """<div style="margin-top: 0px; padding: 0px 10vw; display: flex; border-radius: 5px; border: 0px solid #333; font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace; font-size: 1.2vw;">
    <div style="flex: 1; padding: 10px;">
        <h2>DATA ENGINEER</h2>
        <p>$par1</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 1; padding: 10px;">
        <p>$par2</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 1; padding: 10px;">
        <p>$par3</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 1; padding: 10px;">
        <p>$par4</p>
        <p>Window height: <span id="height-display"></span></p>
    </div>
    <script>
    function updateHeightDisplay() {
        document.getElementById("height-display").textContent = pageHeight;
    }
    updateHeightDisplay();
    window.addEventListener("resize", updateHeightDisplay);
</script>
</div>
""").substitute(par1=get_text_by_name("bio_par1", language), par2=get_text_by_name("bio_par2", language), par3=get_text_by_name("bio_par3", language), par4=get_text_by_name("bio_par4", language))