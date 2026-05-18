from flask import Flask, request, jsonify
import fitz
import requests
import io

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract():
    try:
        data = request.json
        pdf_url = data.get('pdf_url')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(pdf_url, timeout=30, headers=headers)
        pdf_file = io.BytesIO(response.content)
        text = ''
        doc = fitz.open(stream=pdf_file, filetype='pdf')
        for page in doc:
            text += page.get_text() + '\n'
        doc.close()
        return jsonify({'text': text, 'error': False})
    except Exception as e:
        return jsonify({'text': '', 'error': True, 'message': str(e)})

if __name__ == '__main__':
    app.run()
