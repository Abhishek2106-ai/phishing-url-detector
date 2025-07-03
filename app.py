from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# In-memory scan history with some dummy data
scan_history = [
    {
        'url': 'http://malicious-login.tk',
        'prediction': 1,
        'timestamp': '2025-07-03 02:40 PM'
    },
    {
        'url': 'https://github.com',
        'prediction': 0,
        'timestamp': '2025-07-03 02:50 PM'
    },
    {
        'url': 'http://bit.ly/fakelink',
        'prediction': 1,
        'timestamp': '2025-07-03 03:10 PM'
    },
]

def is_phishing(url):
    suspicious_keywords = ['@', 'bit.ly', 'tinyurl', 'xyz', 'tk']
    return 1 if any(keyword in url for keyword in suspicious_keywords) else 0

@app.route('/')
def home():
    return "✅ Phishing Detector Backend is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '')
    prediction = is_phishing(url)

    # Add timestamp to history entry
    scan_history.insert(0, {
        'url': url,
        'prediction': prediction,
        'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M %p')
    })

    # Keep only the last 20
    scan_history[:] = scan_history[:20]

    return jsonify({'prediction': prediction})

@app.route('/history', methods=['GET'])
def history():
    return jsonify(scan_history)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
