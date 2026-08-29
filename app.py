from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "GitOps demo app is running"

@app.route("/version")
def version():
    return "v1"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)