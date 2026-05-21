from string import Template

def get_bio():
    return Template(
"""<div style="margin-top: 0px; padding: 0px 10vw; display: flex; border-radius: 5px; border: 0px solid #333; font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace; font-size: 1.2vw;">
    <div style="flex: 1; padding: 10px;">
        <h2>DATA ENGINEER</h2>
        <p>Software Engineer with a passion for creating innovative solutions and exploring new technologies.</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 1; padding: 10px;">
        <p>With a strong background in full-stack development, I enjoy building scalable applications and contributing to open-source projects.</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 1; padding: 10px;">
        <p>In my free time, I love hiking, photography, and experimenting with new programming languages. I'm always eager to connect with like-minded individuals and collaborate on exciting projects.</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 1; padding: 10px;">
        <p>Feel free to reach out to me on <a href="https://www.linkedin.com/in/jaimecarbosanchez" target="_blank">LinkedIn</a></p>
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
""")