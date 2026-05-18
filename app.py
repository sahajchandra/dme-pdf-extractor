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

        result = response.json()

        if result.get('IsErroredOnProcessing'):
            raise Exception(str(result.get('ErrorMessage')))

        text = '\n'.join(
            page.get('ParsedText', '')
            for page in result.get('ParsedResults', [])
        )

        return jsonify({'text': text, 'error': False})

    except Exception as e:
        return jsonify({'text': '', 'error': True, 'message': str(e)})

if __name__ == '__main__':
    app.run()
