from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class OfflineCodeWriterAgent:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            device_map="auto"
        )
        self.model.eval()

    def generate_code(self, prompt: str, max_tokens: int = 200) -> str:
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.model.device)
        
        # Limit max length to model constraints
        max_length = min(
            input_ids.shape[1] + max_tokens,
            self.model.config.max_position_embeddings
        )

        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_length=max_length,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
        result = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return result[len(prompt):].strip()
