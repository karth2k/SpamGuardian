from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

#Read the data
df = pd.read_csv("data/spam.csv", encoding="latin-1")[['v1', 'v2']]
df.columns = ['label', 'text']


#Drop rows with missing data and show sample rows
df.dropna(inplace=True) 
df['label'] = df['label'].map({'ham': 0, 'spam': 1})
print(df.head())

#Hugging Face Dataset
dataset = Dataset.from_pandas(df)

#Bert Tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

#Tokenizing funciton
def tokenize_batch(batch):
    return tokenizer(batch["text"], padding = "max_length", truncation = True)

#Tokenizes dataset
dataset = dataset.map(tokenize_batch, batched = True)

#Train test split
dataset = dataset.train_test_split(test_size=0.2)

#Training args
training_args = TrainingArguments(
    output_dir="./results",                  
    eval_strategy="epoch",                   
    save_strategy="epoch",                  
    logging_strategy="steps",               
    logging_steps=10,
    per_device_train_batch_size=16,        
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    load_best_model_at_end=True,            
    metric_for_best_model="accuracy",        
    save_total_limit=1,                     
    fp16=True,                              
    report_to="none"                         
)
#BERT model
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", 
                                                            num_labels=2)

#Compute metrics function
def compute_metrics(p):
    preds = np.argmax(p.predictions, axis = 1)
    labels = p.label_ids
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="binary")
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

#trtianing loop funciton
trainer = Trainer(
    model = model,
    args = training_args,
    train_dataset = dataset['train'],
    eval_dataset=dataset['test'],
    tokenizer = tokenizer,
    compute_metrics=compute_metrics
)

#Trains
trainer.train()

#Results
eval_results = trainer.evaluate()
print(f"Final Evaluation Accuracy: {eval_results['eval_accuracy']:.4f}")
print(f"F1 Score: {eval_results['eval_f1']:.4f}")
print(f"Precision: {eval_results['eval_precision']:.4f}")
print(f"Recall: {eval_results['eval_recall']:.4f}")

#Saves model and tokenizer
model.save_pretrained("./model")
tokenizer.save_pretrained("./model")

