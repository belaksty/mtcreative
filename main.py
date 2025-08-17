from flask import Flask, request, send_file
from rembg import new_session
from PIL import Image
import io

session = new_session('u2net')
app = Flask(__name__)

@app.route("/healthz")
def health():
    return "OK", 200

@app.route("/remove-background", methods=["POST"])
def remove_background():
    if "file" not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files["file"]
    img_bytes = file.read()
    result = session.process(img_bytes)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return send_file(output, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)