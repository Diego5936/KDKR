from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

# Route 1: serve the demo page at /sim
@app.route("/sim")
def sim_page():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>KDKR Sim Demo</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
        <link rel="stylesheet" href="/sim/styles.css">
      </head>
      <body>
        <h1 style="text-align:center;">🚁 KDKR Simulation Demo</h1>
        <div id="host" style="max-width:900px;margin:0 auto;"></div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script type="module" src="/sim/index.js"></script>
      </body>
    </html>
    """)

# Route 2: serve the JS/CSS from frontend/sim/src
@app.route("/sim/<path:filename>")
def sim_static(filename):
    return send_from_directory("sim/src", filename)

if __name__ == "__main__":
    app.run(debug=True)