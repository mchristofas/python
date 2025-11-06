#!/usr/bin/env python3
from flask import Flask, render_template_string, request, Response
import subprocess, platform, time, csv, io, json, socket

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Ping Check CSV</title>
<style>
body { font-family: 'Segoe UI', sans-serif; background: #f4f6f8; margin: 0; padding: 0; }
.container { max-width: 700px; margin: 60px auto; background: #fff; padding: 30px 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
h1 { text-align: center; color: #333; margin-bottom: 25px; }
textarea { width: 100%; height: 120px; padding: 10px; border-radius: 8px; border: 1px solid #ccc; resize: vertical; }
button { display: block; width: 100%; margin-top: 15px; padding: 12px; background: #007bff; color: white; font-size: 16px; border: none; border-radius: 8px; cursor: pointer; transition: background 0.3s ease; }
button:hover { background: #0056b3; }
.progress-container { width: 100%; background: #e5e7eb; height: 10px; border-radius: 5px; margin-top: 20px; overflow: hidden; }
.progress-bar { width: 0%; height: 100%; background: #007bff; transition: width 0.4s ease; }
table { width: 100%; border-collapse: collapse; margin-top: 25px; }
th, td { border-bottom: 1px solid #ddd; padding: 10px 12px; text-align: left; }
th { background: #f1f3f5; color: #555; }
.active { color: #16a34a; font-weight: 600; }
.inactive { color: #dc2626; font-weight: 600; }
#exportBtn { display: none; background-color: #16a34a; margin-top: 15px; }
#exportBtn:hover { background-color: #15803d; }
</style>
</head>
<body>
<div class="container">
  <h1>Ping Check + CSV</h1>
  <form id="pingForm">
    <textarea id="ips" placeholder="192.168.1.1&#10;google.com"></textarea>
    <button type="submit">Start Checking</button>
  </form>

  <div class="progress-container" style="display:none;">
    <div class="progress-bar" id="progressBar"></div>
  </div>

  <table id="resultsTable" style="display:none;">
    <thead><tr><th>Host</th><th>Hostname</th><th>Status</th></tr></thead>
    <tbody id="resultsBody"></tbody>
  </table>

  <button id="exportBtn" onclick="downloadCSV()">Download CSV</button>
</div>

<script>
const resultsBody = document.getElementById("resultsBody");
const resultsTable = document.getElementById("resultsTable");
const progressBar = document.getElementById("progressBar");
const progressContainer = document.querySelector(".progress-container");
const exportBtn = document.getElementById("exportBtn");

let lastResults = [];

document.getElementById("pingForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const ipsText = document.getElementById("ips").value.trim();
  if (!ipsText) return;

  const ips = ipsText.split(/\\r?\\n/).filter(line => line.trim() !== "");
  resultsBody.innerHTML = "";
  resultsTable.style.display = "table";
  progressContainer.style.display = "block";
  exportBtn.style.display = "none";
  progressBar.style.width = "0%";
  lastResults = [];

  const evtSource = new EventSource("/ping_stream?" + new URLSearchParams({ ips: ipsText }));
  let doneCount = 0;

  evtSource.onmessage = (event) => {
    const msg = event.data.trim();
    if (msg === "[DONE]") {
      evtSource.close();
      exportBtn.style.display = "block";
      return;
    }
    const [ip, hostname, status] = msg.split(",");
    if (!ip || !status) return;

    lastResults.push({ ip, hostname, status });

    const row = document.createElement("tr");
    row.innerHTML = `<td>${ip}</td><td>${hostname}</td><td class="${status}">${status}</td>`;
    resultsBody.appendChild(row);

    doneCount++;
    progressBar.style.width = ((doneCount / ips.length) * 100).toFixed(1) + "%";
  };
});

async function downloadCSV() {
  const res = await fetch("/export_csv", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ results: lastResults })
  });
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "ping_results.csv";
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}
</script>
</body>
</html>
"""

def ping_host(ip):
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", "2000", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "2", ip]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "N/A"

@app.route("/")
def index():
    return render_template_string(TEMPLATE)

@app.route("/ping_stream")
def ping_stream():
    ips_text = request.args.get("ips", "")
    ips = [line.strip() for line in ips_text.splitlines() if line.strip()]

    def generate():
        for ip in ips:
            ok = ping_host(ip)
            status = "active" if ok else "inactive"
            hostname = resolve_hostname(ip)
            yield f"data: {ip},{hostname},{status}\n\n"
            time.sleep(0.2)
        yield "data: [DONE]\n\n"

    return Response(generate(), mimetype="text/event-stream")

@app.route("/export_csv", methods=["POST"])
def export_csv():
    data = request.get_json(force=True)
    results = data.get("results", [])
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Host", "Hostname", "Status"])
    for r in results:
        writer.writerow([r.get("ip", ""), r.get("hostname", ""), r.get("status", "")])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=ping_results.csv"},
    )

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
