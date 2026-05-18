from flask import Flask, request, jsonify
import pdfplumber
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
        content_type = response.headers.get('Content-Type', '')
        content_length = len(response.content)
        
        pdf_file = io.BytesIO(response.content)
        text = ''
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
        return jsonify({
            'text': text,
            'error': False,
            'debug_content_type': content_type,
            'debug_content_length': content_length
        })
    except Exception as e:
        return jsonify({'text': '', 'error': True, 'message': str(e)})

if __name__ == '__main__':
    app.run()
