from string import Template

def get_template():

    return Template(
"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Jaime Carbó — Data Engineer</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%23111'/><path d='M2 7 L5 6 L8 19 L10 28 L13 20 L16 7 L19 6 L22 19 L24 28 L27 20 L30 7' stroke='%23fff' stroke-width='2' fill='none' stroke-linecap='round'><animate attributeName='d' values='M2 7 L5 6 L8 19 L10 28 L13 20 L16 7 L19 6 L22 19 L24 28 L27 20 L30 7;M2 12 L5 4 L8 13 L10 26 L13 25 L16 12 L19 4 L22 13 L24 26 L27 25 L30 12;M2 18 L5 5 L8 8 L10 22 L13 28 L16 18 L19 5 L22 8 L24 22 L27 28 L30 18;M2 23 L5 9 L8 4 L10 15 L13 27 L16 23 L19 9 L22 4 L24 15 L27 27 L30 23;M2 27 L5 15 L8 4 L10 10 L13 24 L16 27 L19 15 L22 4 L24 10 L27 24 L30 27;M2 28 L5 21 L8 7 L10 5 L13 18 L16 28 L19 21 L22 7 L24 5 L27 18 L30 28;M2 25 L5 26 L8 13 L10 4 L13 12 L16 25 L19 26 L22 13 L24 4 L27 12 L30 25;M2 20 L5 28 L8 19 L10 6 L13 7 L16 20 L19 28 L22 19 L24 6 L27 7 L30 20;M2 14 L5 27 L8 24 L10 10 L13 4 L16 14 L19 27 L22 24 L24 10 L27 4 L30 14;M2 9 L5 23 L8 28 L10 17 L13 5 L16 9 L19 23 L22 28 L24 17 L27 5 L30 9;M2 5 L5 17 L8 28 L10 22 L13 8 L16 5 L19 17 L22 28 L24 22 L27 8 L30 5;M2 4 L5 11 L8 25 L10 27 L13 14 L16 4 L19 11 L22 25 L24 27 L27 14 L30 4;M2 7 L5 6 L8 19 L10 28 L13 20 L16 7 L19 6 L22 19 L24 28 L27 20 L30 7' dur='1.5s' repeatCount='indefinite'/></path></svg>">
    <style>html { height: 100%; } body { min-height: 100vh; overflow-y: auto; margin: 0; font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace; font-size: 1.2vw; } pre { font-family: inherit; font-size: inherit; }</style>
</head>
$header
$lang_selector
$bio
$cluster
$mongodb
<script>
    (function() {
        const sessionId = crypto.randomUUID();
        const dwellTimers = {};
        const lastVisible = {};
        function sendBeacon(url, data) {
            navigator.sendBeacon(url, new Blob([JSON.stringify(data)], { type: "application/json" }));
        }
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const section = entry.target.getAttribute("data-track");
                if (entry.isIntersecting) {
                    lastVisible[section] = Date.now();
                } else if (lastVisible[section]) {
                    dwellTimers[section] = (dwellTimers[section] || 0) + Date.now() - lastVisible[section];
                    delete lastVisible[section];
                }
            });
        }, { threshold: 0.5 });
        document.querySelectorAll("[data-track]").forEach(el => observer.observe(el));
        document.querySelectorAll("[data-track-click]").forEach(el => {
            el.addEventListener("click", () => {
                const section = el.getAttribute("data-track-click");
                sendBeacon("/metrics", { type: "click", section: section, session_id: sessionId });
            });
        });
        window.addEventListener("beforeunload", () => {
            document.querySelectorAll("[data-track]").forEach(el => {
                const section = el.getAttribute("data-track");
                let duration = dwellTimers[section] || 0;
                if (lastVisible[section]) {
                    duration += Date.now() - lastVisible[section];
                }
                if (duration > 0) {
                    sendBeacon("/metrics", { type: "dwell", section: section, duration_ms: duration, session_id: sessionId });
                }
            });
        });
    })();
</script>
</body>
</html>
""")

