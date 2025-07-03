from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# In-memory scan history
scan_history = []

# Dummy phishing check function
def is_phishing(url):
    suspicious_keywords = ['@', 'bit.ly', 'tinyurl', 'xyz', 'tk']
    return 1 if any(keyword in url for keyword in suspicious_keywords) else 0

# ✅ Root route to confirm backend is running
@app.route('/')
def home():
    return "✅ Phishing Detector Backend is running!"

# 🚀 Predict route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '')
    prediction = is_phishing(url)

    # Save to history
    scan_history.insert(0, {
        'url': url,
        'prediction': prediction,
        'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M %p')
    })

    # Keep only last 20 entries
    scan_history[:] = scan_history[:20]

    return jsonify({'prediction': prediction})

# 📜 History route
@app.route('/history', methods=['GET'])
def history():
    return jsonify(scan_history)

# 🔥 Run the app (Render uses dynamic port)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
