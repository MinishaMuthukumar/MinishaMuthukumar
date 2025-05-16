from flask import Flask, render_template, request

app = Flask(__name__)

# Simple list of phishing keywords
phishing_keywords = [
    "urgent", "verify your account", "password expired", "click here", 
    "account suspended", "login immediately", "update your information", 
    "confirm your identity", "you have won", "limited time offer"
]

def is_phishing(email_text):
    email_text = email_text.lower()
    for keyword in phishing_keywords:
        if keyword in email_text:
            return True
    return False

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        email_content = request.form["email"]
        if is_phishing(email_content):
            result = "Warning: This email might be a phishing attempt!"
        else:
            result = "This email appears to be safe."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
