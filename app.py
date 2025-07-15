import os
from flask import Flask, render_template, request
from datetime import datetime
from utils.ocr_utils import extract_text_from_image, extract_expiry_date
from utils.match_utils import load_medicine_dataframe, fuzzy_match

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    verdict = ""
    matches = []
    expired = False
    input_type = request.form['input_type']
    df = load_medicine_dataframe()

    if input_type == 'image':
        file = request.files['image']
        if file:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            text = extract_text_from_image(path)
            expiry_date = extract_expiry_date(text)
            if expiry_date and expiry_date < datetime.now():
                expired = True
            print(text, expiry_date)
            matches = fuzzy_match(text, df)
    else:
        text = request.form['med_name']
        matches = fuzzy_match(text, df)
        expiry_date = None

    if matches:
        if expired:
            verdict = "⚠️ Expired & Valid"
        else:
            verdict = "✅ Valid"
    else:
        verdict = "❌ Fake"
        if expired:
            verdict = "❌ Fake & ⚠️ Expired"

    return render_template('result.html', text=text, matches=matches, verdict=verdict, expiry=expiry_date)

if __name__ == '__main__':
    app.run(debug=True)
