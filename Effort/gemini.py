from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# The URL of your Node.js summarization service
NODE_SERVER_URL = "http://localhost:3000/summarize"

@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    article = request.form["article"]
    
    try:
        # Send request to Node.js server
        response = requests.post(NODE_SERVER_URL, json={"text": article})
        response.raise_for_status()
        
        summary = response.json().get("summary", "No summary returned.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        summary = "Error generating summary."
    
    return render_template("summary2.html", article=article, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
