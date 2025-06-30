from flask import Flask, request, jsonify
import torch
from transformers import BertTokenizer, BertForSequenceClassification

app = Flask(__name__)

#Load model and tokenizer at startup
model_path = "./model"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()

#Loading Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


#Gets prediction
def predict(text):
    inputs = tokenizer(text, return_tensors="pt", padding = True, truncation = True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        pred = torch.argmax(logits, dim = 1).item()
        label = "This message is most likely spam." if pred == 1 else "This message is most likely NOT spam."
        return label
    
#API Endpoint
@app.route("/predict", methods = ["POST"])
def predict_route():
    data = request.get_json()
    if "text" not in data:
        return jsonify({"Error occured: Missing 'text' field"}), 400
    
    text = data["text"]
    label = predict(text)
    return jsonify({"label": label})


#Run Application
if __name__ == "__main__":
    app.run(debug=True)