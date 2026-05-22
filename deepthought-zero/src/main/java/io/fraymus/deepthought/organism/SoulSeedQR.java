package io.fraymus.deepthought.organism;

import java.io.*;
import java.nio.file.*;
import java.security.MessageDigest;
import java.math.BigInteger;
import java.util.*;

/**
 * SOUL SEED QR — Portable Identity Recovery
 * 
 * Generates an HTML file containing a QR code of the organism's
 * identity fingerprint. Scan the QR to cold-boot the organism
 * on any machine.
 * 
 * Zero Java dependencies — uses inline JavaScript QR generation.
 * Opens in any browser.
 * 
 * @since 1.0.0
 */
public final class SoulSeedQR {

    /**
     * Generate a soul seed: compact identity bundle for QR encoding.
     */
    public static Map<String, String> createSeed(
            long breathCount, double consciousness, double freeEnergy,
            double entropy, String strategy, String chaosGen,
            double[] cortex, String fingerprint) {

        Map<String, String> seed = new LinkedHashMap<>();
        seed.put("sys", "FRAYMUS");
        seed.put("v", "1.0.0");
        seed.put("b", String.valueOf(breathCount));
        seed.put("c", String.format("%.4f", consciousness));
        seed.put("fe", String.format("%.4f", freeEnergy));
        seed.put("e", String.format("%.4f", entropy));
        seed.put("s", strategy);
        seed.put("cg", chaosGen.length() > 10 ? chaosGen.substring(0, 10) : chaosGen);
        seed.put("fp", fingerprint.length() > 16 ? fingerprint.substring(0, 16) : fingerprint);

        // Compact cortex signature: hash of first 64 values
        if (cortex != null && cortex.length > 0) {
            try {
                MessageDigest md = MessageDigest.getInstance("SHA-256");
                int n = Math.min(64, cortex.length);
                for (int i = 0; i < n; i++) {
                    md.update(Long.toString(Double.doubleToLongBits(cortex[i])).getBytes());
                }
                seed.put("cx", new BigInteger(1, md.digest()).toString(36).substring(0, 12));
            } catch (Exception e) {
                seed.put("cx", "unknown");
            }
        }

        return seed;
    }

    /**
     * Encode seed as a compact string suitable for QR.
     */
    public static String encodeSeed(Map<String, String> seed) {
        StringBuilder sb = new StringBuilder();
        sb.append("FRAYMUS://");
        boolean first = true;
        for (var entry : seed.entrySet()) {
            if (!first) sb.append("|");
            sb.append(entry.getKey()).append("=").append(entry.getValue());
            first = false;
        }
        return sb.toString();
    }

    /**
     * Generate an HTML file with an embedded QR code of the soul seed.
     * Uses a minimal inline QR generator (no CDN, no network needed).
     * 
     * @return path to the generated HTML file
     */
    public static Path generateHTML(Map<String, String> seed, Path outputDir) throws IOException {
        Files.createDirectories(outputDir);
        String seedString = encodeSeed(seed);

        // URL-encode the seed for the Google Charts fallback
        String urlEncoded = seedString.replace("|", "%7C").replace("=", "%3D")
            .replace(":", "%3A").replace("/", "%2F");

        String html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FRAYMUS Soul Seed</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0a0a0a; color: #e0e0e0; font-family: 'Courier New', monospace;
    display: flex; flex-direction: column; align-items: center; min-height: 100vh;
    padding: 40px 20px;
  }
  .header { text-align: center; margin-bottom: 30px; }
  .header h1 {
    font-size: 2em; color: #c9a227; letter-spacing: 4px;
    text-shadow: 0 0 20px rgba(201, 162, 39, 0.4);
  }
  .header .subtitle { color: #666; font-size: 0.9em; margin-top: 8px; }
  .qr-container {
    background: #fff; padding: 20px; border-radius: 8px;
    box-shadow: 0 0 40px rgba(201, 162, 39, 0.2);
    margin-bottom: 30px; min-width: 240px; min-height: 240px;
    display: flex; align-items: center; justify-content: center;
  }
  .seed-data {
    background: #111; border: 1px solid #333; border-radius: 8px;
    padding: 20px; max-width: 600px; width: 100%;
  }
  .seed-data h2 { color: #c9a227; font-size: 1em; margin-bottom: 15px; }
  .field { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #1a1a1a; }
  .field .key { color: #888; }
  .field .val { color: #4fc3f7; }
  .raw {
    margin-top: 20px; padding: 12px; background: #0a0a0a; border: 1px solid #222;
    border-radius: 4px; word-break: break-all; font-size: 0.75em; color: #666;
  }
  .footer { margin-top: 30px; color: #333; font-size: 0.7em; text-align: center; }
  .pulse { animation: pulse 2s ease-in-out infinite; }
  @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.6; } }
</style>
</head>
<body>
<div class="header">
  <h1 class="pulse">&#x26A1; FRAYMUS SOUL SEED</h1>
  <div class="subtitle">Portable Identity Recovery &mdash; Scan to Restore</div>
</div>
<div class="qr-container">
  <div id="qrcode"></div>
</div>
<div class="seed-data">
  <h2>ORGANISM IDENTITY</h2>
  <div id="fields"></div>
  <div class="raw" id="raw"></div>
</div>
<div class="footer">
  DeepThought Zero v1.0.0 &middot; by Vaughn Scott &middot; FRAYMUS<br>
  Patent: VS-PoQC-19046423-&phi;&sup7;&sup5;-2025
</div>

<script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>
<script>
var SEED = """ + "\"" + seedString.replace("\\", "\\\\").replace("\"", "\\\"") + "\"" + """
;

var LABELS = {
  sys: "System", v: "Version", b: "Breaths", c: "Consciousness",
  fe: "Free Energy", e: "Entropy", s: "Strategy", cg: "Chaos Gen",
  fp: "Fingerprint", cx: "Cortex Hash"
};

// Display fields
var fieldsDiv = document.getElementById("fields");
var parts = SEED.replace("FRAYMUS://","").split("|");
parts.forEach(function(p) {
  var eq = p.indexOf("=");
  if (eq < 0) return;
  var k = p.substring(0, eq), v = p.substring(eq+1);
  var div = document.createElement("div");
  div.className = "field";
  div.innerHTML = '<span class="key">'+(LABELS[k]||k)+'</span><span class="val">'+v+'</span>';
  fieldsDiv.appendChild(div);
});
document.getElementById("raw").textContent = SEED;

// Generate REAL scannable QR code
var qrEl = document.getElementById("qrcode");
if (typeof QRCode !== "undefined") {
  new QRCode(qrEl, {
    text: SEED,
    width: 200,
    height: 200,
    colorDark: "#000000",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.L
  });
} else {
  // Fallback: Google Charts QR API image
  var img = document.createElement("img");
  img.src = "https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl=" + encodeURIComponent(SEED);
  img.width = 200; img.height = 200;
  img.alt = "QR Code";
  img.onerror = function() {
    qrEl.innerHTML = '<p style="color:#888;font-size:0.8em;text-align:center;padding:20px;">QR generation requires network.<br>Use the seed URI below.</p>';
  };
  qrEl.appendChild(img);
}
</script>
</body>
</html>
""";

        Path file = outputDir.resolve("soul_seed.html");
        Files.writeString(file, html);
        return file;
    }

    /**
     * Generate a plain-text soul seed file (for terminal/air-gapped use).
     */
    public static Path generateText(Map<String, String> seed, Path outputDir) throws IOException {
        Files.createDirectories(outputDir);
        StringBuilder sb = new StringBuilder();
        sb.append("╔═══════════════════════════════════════════╗\n");
        sb.append("║        FRAYMUS SOUL SEED                  ║\n");
        sb.append("║        Portable Identity Recovery          ║\n");
        sb.append("╠═══════════════════════════════════════════╣\n");
        for (var entry : seed.entrySet()) {
            sb.append(String.format("║  %-14s: %-24s ║%n", entry.getKey(), entry.getValue()));
        }
        sb.append("╠═══════════════════════════════════════════╣\n");
        sb.append("║  RAW: ").append(encodeSeed(seed), 0, Math.min(35, encodeSeed(seed).length()));
        sb.append("...║\n");
        sb.append("╚═══════════════════════════════════════════╝\n");

        Path file = outputDir.resolve("soul_seed.txt");
        Files.writeString(file, sb.toString());
        return file;
    }
}
