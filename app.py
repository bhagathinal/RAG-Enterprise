from flask import Flask,request,jsonify,render_template
from Source.pipeline_5 import run_pipeline

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask",methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error" : "Question is required"}), 400
    return jsonify(run_pipeline(question))

if __name__=="__main__":
    app.run(debug=True) 