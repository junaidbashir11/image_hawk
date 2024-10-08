from transformers import CLIPProcessor, CLIPModel
from transformers import BertTokenizer, FlavaModel
import torch

class TextEmbeddingEngine():
    def __init__(self,text,model_type):
        # Initialize the model and processor once
        self.model_type=model_type
        self.text=text

    def __get_text_embedding(self,text):
        """Private method to get the embedding for a single text."""
        
        if self.model_type=="clip":

            model=CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

            inputs =processor(text=text, return_tensors="pt")
            with torch.no_grad():
                embedding =model.get_text_features(**inputs).numpy()
            return embedding.squeeze()
        
        elif self.model_type=="flava":

            model = FlavaModel.from_pretrained("facebook/flava-full")
            tokenizer = BertTokenizer.from_pretrained("facebook/flava-full")
            inputs = tokenizer(text=[text], return_tensors="pt", padding="max_length", max_length=77)
            text_embedding = model.get_text_features(**inputs)
            return text_embedding
        
        else:
            print("other models not supported yet")

    def get_embedding_for_text(self):
        """Public method to expose the text embedding."""
        return self.__get_text_embedding(self.text)