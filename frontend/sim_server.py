from flask import Flask, send_from_directory, render_template_string, jsonify
import os, runpy

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
SIM_DIR = os.path.abspath(os.path.join(BASE_DIR, "sim"))

# --- Load sim/data_model.py by path, no packages/caches involved ---
# dm_path = os.path.join(SIM_DIR, "data_model.py")
# if not os.path.exists(dm_path):
#     raise FileNotFoundError(f"data_model.py not found at {dm_path}")

dm_path = os.path.join(SIM_DIR, "data_model.py")
print("DEBUG dm_path:", dm_path)
print("DEBUG exists:", os.path.exists(dm_path))
try:
    print("DEBUG size:", os.path.getsize(dm_path))
    with open(dm_path, "r", encoding="utf-8") as f:
        head = f.read(300)
    print("DEBUG head:\n", head)
except Exception as e:
    print("DEBUG could not read file:", e)


ns = runpy.run_path(dm_path)          # executes the file and returns its globals as a dict
if "build_mission_view" not in ns:
    # Help debug if the function isn't present
    raise RuntimeError(
        f"`build_mission_view` not found in {dm_path}. "
        f"Available names: {sorted(k for k in ns.keys() if not k.startswith('__'))}"
    )
build_mission_view = ns["build_mission_view"]
# -------------------------------------------------------

DEMO_HTML = os.path.join(BASE_DIR, "sim", "demo", "index.html")
SIM_SRC = os.path.join(BASE_DIR, "sim", "src")

# Sim page
@app.route("/sim")
def sim_page():
    with open(DEMO_HTML, "r", encoding="utf-8") as f:
        return render_template_string(f.read())

# Frontend
@app.route("/sim/<path:filename>")
def sim_static(filename):
    return send_from_directory(SIM_SRC, filename)

@app.route("/mission_view/<int:mission_id>")
def mission_view(mission_id):
    try:
        view = build_mission_view(mission_id)
        if not view:
            return jsonify({"error": "Mission not found"}), 404
        return jsonify(view)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": "internal", "detail": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)