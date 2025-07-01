# SpamGuardian

## Background
I wanted to create a checker that can determine whether or not a piece of text is spam. 

## Implementation
I first began by researching on transformers and stumbled upon BERT/DistilBERT. I then finetuned the DistilBERT Model from Hugging Face by preprocessing a spam classification dataset to be loaded and trained on by the model. Also I used the Hugging Face DistilBERT tokenizer. After training, the model was able to detect spam with an accuracy of 99.7%. I then saved the model locally and created a Flask Backend which predicts whether or not the user inputted text is spam or not by calling a function predict which uses PyTorch and gets a prediction from the model saved locally. I then built a React frontend in the form of a chat message application so that the user can paste text into the chatbox and the model would reply to the text specifying whether it was most likely spam or not.

## Usage (For Now)
1. Download Repository locally
2. Create a folder labeled "model" within the SpamGuardian folder
3. In the terminal (can first create a virtual environment if needed) do `pip install -r requirements.txt`
4. Go into the backend/ folder Run train_model.py (it should finetune the DistilBERT Model from transformers and save it within the model/ folder)
5. Next run the Flask server by doing `python app.py` within the backend/ server.
6. Next within the frontend/ folder do `npm run dev` within the terminal. 
7. Open the locally hosted server and try it out!

## Next Steps
Host backend/frontend online.