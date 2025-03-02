import json
from flask import Flask, render_template, request
from sentiment_analysis import sentiment_analyzer

app = Flask("Sentiment Analyzer")
@app.route("/sentimentAnalyzer")
@app.route("/sentimentAnalyzer")
def sent_analyzer():
    try:
        text_to_analyze = request.args.get('textToAnalyze')

        if not text_to_analyze:
            return {"error": "Missing 'textToAnalyze' parameter"}, 400

        # Run sentiment analysis
        response = sentiment_analyzer(text_to_analyze)

        print("🔍 Response from sentiment_analyzer():", response)  # Debugging log
        # Ensure response format is correct
        if not isinstance(response, dict) or "documentSentiment" not in response:
            return {"error": "Invalid response from sentiment_analyzer", "details": str(response)}, 500

        label = response["documentSentiment"].get('label', 'unknown')
        score = response["documentSentiment"].get('score', 0)

        print(f"🔍 Extracted label: {label}, score: {score}")  # Debugging log

        # Ensure label format is correct
        label_parts = label.split('_')
        if len(label_parts) > 1:
            label = label_parts[1]  # This might be unnecessary since label is already 'positive'

        return {
            "message": f"The given text has been identified as {label} with a score of {score}."
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")  # Print error to Flask logs
        return {"error": "Internal Server Error", "details": str(e)}, 500


@app.route("/")
def render_index_page():
    return render_template('index.html')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)