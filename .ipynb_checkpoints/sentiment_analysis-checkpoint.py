import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class BertSentimentAnalyzer:
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        """Load tokenizer and model once at initialization"""
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.id2label = self.model.config.id2label

        self.label_mapping = {
            "POSITIVE": "positive",
            "NEGATIVE": "negative",
            "NEUTRAL": "neutral"
        }

    def analyze_sentiment(self, text):
        """Analyze sentiment using the loaded BERT model"""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.nn.functional.softmax(outputs.logits, dim=1)

        predicted_class_id = scores.argmax().item()
        predicted_label = self.id2label[predicted_class_id]
        confidence_score = scores[0][predicted_class_id].item()

        return self.label_mapping.get(predicted_label, predicted_label.lower()), confidence_score

# Load the model once and reuse it
analyzer = BertSentimentAnalyzer()

def sentiment_analyzer(text_to_analyse):
    """Analyze text and return structured response"""
    doc_label, doc_score = analyzer.analyze_sentiment(text_to_analyse)

    response = {
        "documentSentiment": {
            "label": doc_label,
            "score": doc_score
        }
    }
    return response
