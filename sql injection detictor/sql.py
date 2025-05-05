from flask import Flask, render_template_string, request
import re
import logging
from datetime import datetime
import os

app = Flask(_name_)

# Set up logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "detections.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

# SQL injection patterns
sql_injection_patterns = [
    r"(?i)(\%27)|(\')|(\-\-)|(\%23)|(#)",
    r"(?i)(\%22)|(\")|(\%3D)|(=)",
    r"(?i)(\bOR\b|\bAND\b).*(=|\blike\b|\bis\b)",
    r"(?i)UNION(\s)+SELECT",
    r"(?i)SELECT(\s)+.*FROM",
    r"(?i)INSERT(\s)+INTO",
    r"(?i)UPDATE(\s)+.*SET",
    r"(?i)DELETE(\s)+FROM",
    r"(?i)DROP(\s)+TABLE",
    r"(?i)(\%27)|(\')(\s)OR(\s)('1'='1')"
]

def is_sql_injection(input_str):
    for pattern in sql_injection_patterns:
        if re.search(pattern, input_str):
            return True
    return False

# HTML Template
template = """<!doctype html>
<title>SQL Injection Detector</title>
<h2>SQL Injection Detection Tool</h2>
<form method="post">
    <input name="user_input" style="width:300px" placeholder="Enter user input">
    <button type="submit">Check</button>
</form>
{% if result is not none %}
    <p style="color: {{ 'red' if result else 'green' }}">
        SQL Injection Detected: {{ 'Yes' if result else 'No' }}
    </p>
{% endif %}"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        result = is_sql_injection(user_input)
        log_message = f"Input: {user_input} --> SQL Injection: {'YES' if result else 'NO'}"
        logging.info(log_message)
    return render_template_string(template, result=result)

if _name_ == "_main_":
    app.run(debug=True)
