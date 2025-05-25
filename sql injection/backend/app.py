from flask import Flask, request, jsonify
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin for frontend communication

# Simple SQLi detection function using regex
def detect_sql_injection(user_input):
    sql_keywords = [
        "select", "union", "insert", "drop", "update", "--", ";", "' or", '" or', "' and", '" and'
    ]
    pattern = '|'.join([re.escape(keyword) for keyword in sql_keywords])
    return bool(re.search(pattern, user_input, re.IGNORECASE))

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    user_input = data.get('input', '')

    if detect_sql_injection(user_input):
        return jsonify({'result': 'injection'})
    else:
        return jsonify({'result': 'safe'})

if __name__ == '__main__':
    app.run(debug=True)
