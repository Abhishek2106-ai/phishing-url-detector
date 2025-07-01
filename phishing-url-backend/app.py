from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory history list
scan_history = []

def is_phishing(url):
    """
    Replace this logic with your real ML model.
    For now, returns 1 if suspicious, else 0.
    """
    suspicious_keywords = ['@', 'bit.ly', 'tinyurl', 'xyz', 'tk']
    if any(keyword in url for keyword in suspicious_keywords):
        return 1
    return 0

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '')

    prediction = is_phishing(url)
    
    # Store in history
    scan_history.insert(0, {
        'url': url,
        'prediction': prediction,
        'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M %p')
    })
    
    # Limit history to last 20 entries
    scan_history[:] = scan_history[:20]

    return jsonify({'prediction': prediction})

@app.route('/history', methods=['GET'])
def history():
    return jsonify(scan_history)

if __name__ == '__main__':
    app.run(debug=True)
