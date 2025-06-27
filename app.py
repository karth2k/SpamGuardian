from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load model and tokenizer
model_path = "./model"  # path to the folder where you saved the model
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()  # set model to evaluation mode

# Set to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Function to predict
def predict(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    inputs = {key: val.to(device) for key, val in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        label = "spam" if predicted_class == 1 else "good"
        return label

# Example
text = "Hey, I just transferred you $20 on Venmo for lunch yesterday — let me know if you got it!"
result = predict(text)
print(f"Prediction: {result}")
