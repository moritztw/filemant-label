from flask import Flask, render_template_string, request, send_file
import io
import urllib.parse
from jinja2 import Template
from weasyprint import HTML
from pdf2image import convert_from_path
import tempfile
import os

app = Flask(__name__)

# HTML-Formular für den Browser
FORM_HTML = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Filament Label Generator (40x30mm)</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f4f4f9; padding: 20px; color: #333; }
        .container { max-width: 500px; margin: 0 auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h2 { margin-top: 0; color: #111; font-size: 20px; }
        .form-group { margin-bottom: 12px; }
        label { display: block; font-size: 12px; font-weight: bold; margin-bottom: 4px; color: #555; }
        input { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
        .row { display: flex; gap: 10px; }
        .row .form-group { flex: 1; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🏷️ Filament Label Generator</h2>
        <form action="/generate" method="POST">
            <div class="row">
                <div class="form-group"><label>Hersteller (Brand):</label><input type="text" name="brand" value="Bambu Lab" required></div>
                <div class="form-group"><label>HEX-Code:</label><input type="text" name="hex" value="#FFFFFF"></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Material:</label><input type="text" name="material" value="PETG HF" required></div>
                <div class="form-group"><label>Farbe:</label><input type="text" name="color" value="White (33100)"></div>
            </div>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 15px 0;">
            <div class="row">
                <div class="form-group"><label>Nozzle Temp:</label><input type="text" name="nozzle" value="230-260°C"></div>
                <div class="form-group"><label>Bed Temp:</label><input type="text" name="bed" value="65-75°C"></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Flow Rate:</label><input type="text" name="flow" value="0.95"></div>
                <div class="form-group"><label>Pressure Adv:</label><input type="text" name="pressure_adv" value="0.026"></div>
            </div>
            <div class="row">
                <div class="form-group"><label>TD (Transmission Dist.):</label><input type="text" name="td" value="2.9"></div>
                <div class="form-group"><label>QR-Data / URL:</label><input type="text" name="qr_data" value="https://bambulab.com"></div>
            </div>
            <button type="submit">🖼️ PNG Generieren & Herunterladen</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(FORM_HTML)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.to_dict()
    data["urlencode"] = lambda x: urllib.parse.quote(str(x))

    with open("template.html", "r", encoding="utf-8") as f:
        template_src = f.read()

    rendered_html = Template(template_src).render(**data)

    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "temp.pdf")
        HTML(string=rendered_html).write_pdf(pdf_path)

        images = convert_from_path(pdf_path, dpi=300)
        img_io = io.BytesIO()
        images[0].save(img_io, 'PNG')
        img_io.seek(0)

        filename = f"label_{data.get('brand','').replace(' ','_')}_{data.get('material','').replace(' ','_')}.png"
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
