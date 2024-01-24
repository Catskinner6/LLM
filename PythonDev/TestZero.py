# Creating a Python environment for HuggingFace and LLAMA-2
# Author:   Scott Rice
# Created:  2024-01-17
# Updated:  2024-

from transformers import AutoModelForMaskedLM, AutoTokenizer

model_name = "bert-based-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMaskedLM.from_pretrained(model_name)


