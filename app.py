from flask import Flask, request, jsonify
import requests
import pytesseract
from pdf2image import convert_from_bytes

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract():
    try:
        data = request.json
        pdf_url = data.get('pdf_url')
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(pdf_url, timeout=30, headers=headers)
        images = convert_from_bytes(response.content)
        text = ''
        for image in images:
            text += pytesseract.image_to_string(image) + '\n'
        return jsonify({'text': text, 'error': False})
    except Exception as e:
        return jsonify({'text': '', 'error': True, 'message': str(e)})

if __name__ == '__main__':
    app.run()
