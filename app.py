from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract():
    try:
        data = request.json
        pdf_url = data.get('pdf_url')
        api_key = data.get('ocr_api_key')

        response = requests.get(
            'https://api.ocr.space/parse/url',
            params={
                'url': pdf_url,
                'apikey': api_key,
                'language': 'eng',
                'OCREngine': '2',
                'isTable': 'true'
            },
            timeout=60
        )

        return jsonify({
            'debug_status': response.status_code,
            'debug_raw': response.text[:1000],
            'error': False
        })

    except Exception as e:
        return jsonify({'text': '', 'error': True, 'message': str(e)})

if __name__ == '__main__':
    app.run()
