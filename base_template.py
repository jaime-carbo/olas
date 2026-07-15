from string import Template

def get_template():

    return Template(
"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Jaime Carbó — Data Engineer</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%23111'/><path d='M2 16 Q8 4 14 16 T26 16 T30 16' stroke='%23fff' stroke-width='2' fill='none' stroke-linecap='round'/></svg>">
    <style>html { height: 100%; } body { min-height: 100vh; overflow-y: auto; margin: 0; font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace; font-size: 1.2vw; } pre { font-family: inherit; font-size: inherit; }</style>
</head>
$header
$lang_selector
$bio
$experience
$cluster
$mongodb
<div style="padding: 0px 10vw; margin-top: 20px;"><hr style="border: none; border-top: 1px solid #333; margin: 0;"></div>
$resource_history
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

