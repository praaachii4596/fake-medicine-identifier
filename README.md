# Fake Medicine Identifier

A Flask-based web application that helps identify **fake or expired medicines** using OCR and fuzzy matching against the **WHO Essential Medicines List**.

---

## Features

- Upload medicine **label images**
- Or manually **type** a medicine name
- Uses **EasyOCR (CPU)** to extract:
  - Medicine Name
  - Expiry Date (`MM/YYYY`, `DD-MM-YYYY`, etc.)
- Preprocesses image with OpenCV for better accuracy
- Fuzzy matches OCR text to WHO medicine list
- Detects expired medicines
- Provides final verdict:
  - Valid
  - Fake
  - Expired
  - Fake & Expired

---

## Tech Stack

| Layer     | Tech                               |
|-----------|------------------------------------|
| Backend   | Python, Flask                      |
| OCR       | EasyOCR (CPU mode)                 |
| Image     | OpenCV, NumPy                      |
| Matching  | RapidFuzz                          |
| Frontend  | HTML5, Bootstrap 5                 |
| Dataset   | WHO Essential Medicines List 2023  |

---

## Installation

### 1. Clone this repo

```bash
git clone https://github.com/praaachii4596/fake-medicine-identifier.git
cd fake-medicine-identifier
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Flask app
```bash
python app.py
```
Visit http://127.0.0.1:5000 in your browser.

---

## Folder Structure

fake_medicine_identifier/
│
├── app.py
├── requirements.txt
├── README.md
│
├── static/
│   └── uploads/               ← uploaded & processed images
│
├── templates/
│   ├── index.html             ← upload and input form
│   └── result.html            ← verdict and result display
│
├── utils/
│   ├── ocr_utils.py           ← EasyOCR + preprocessing
│   └── match_utils.py         ← fuzzy matching and logic
│   └── clean_who_list.py      ← clean the who_essential_meds_2023.csv
│
├── data/
│   ├── who_essential_meds_2023.csv            ← original (source)
│   └── who_essential_meds_2023_cleaned.csv    ← used in code

---

## How It Works

1. Upload image → OpenCV preprocess → EasyOCR extracts text
2. Use regex to extract expiry date
3. Fuzzy match medicine name (≥85%) to WHO list
4. Show verdict and confidence

---

## Sample Inputs

images/test_paracetamol.jpg
images/bcg_fake_label.jpg
images/expired_strip.jpg

---

## Data Source & Licensing

This project uses the **WHO Electronic Essential Medicines List (eEML)**:

- © World Health Organization, 2023  
- Source: [https://list.essentialmeds.org](https://list.essentialmeds.org)  
- License: [CC BY 3.0 IGO](https://creativecommons.org/licenses/by/3.0/igo/)  
- Proper Attribution:  
  _WHO electronic Essential Medicines List (eEML), World Health Organization, 2023._

**Note:** This project is not affiliated with or endorsed by the World Health Organization.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Built by Prachi Joshi — feel free to fork or suggest improvements!