from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class SentimentModel():

    def __init__(self):

        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(self.device)
        self.labels = ["positive", "negative", "neutral"]

    def find_sentiment(self, news):

        if news:
            tokens = self.tokenizer(news, return_tensors="pt", padding=True).to(self.device)

            result = self.model(tokens["input_ids"], attention_mask=tokens["attention_mask"])[
                "logits"
            ]
            result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
            probability = result[torch.argmax(result)]
            sentiment = self.labels[torch.argmax(result)]
            return probability, sentiment
        
        else:
            return 0, self.labels[-1]