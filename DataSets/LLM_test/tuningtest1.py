# Colab edited for local PC

# Install libraries
# !pip install -q accelerate peft bitsandbytes transformers trl tensorboard huggingface_hub[cli] xformers

# Import Dependencies
import os
import torch
from datasets import load_dataset
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging
)
from peft import LoraConfig
from trl import SFTTrainer
import transformers

# Set the name of the model we'll use for the rest of the notebook
model_name = "meta-llama/Llama-2-7b-chat-hf"

# Load the entire model on the GPU 0
device_map = {"": 0}

# Set base model loading in 4-bits
use_4bit = True

# Compute dtype for 4-bit base models
bnb_4bit_compute_dtype = "float16"

# Quantization type (fp4 or nf4)
bnb_4bit_quant_type = "nf4"

# Activate nested quantization for 4-bit base models (double quantization)
use_nested_quant = False

# Load Model
compute_dtype = getattr(torch, bnb_4bit_compute_dtype)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=use_4bit,
    bnb_4bit_quant_type=bnb_4bit_quant_type,
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=use_nested_quant
)
# Load the base model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map=device_map,
    quantization_config=bnb_config,
)
model.config.use_cache = False
model.config.pretraining_tp = 1

# Load the model tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# Define a custom padding token
tokenizer.pad_token = "<PAD>"

# Set the padding direction to the right
tokenizer.padding_side = "right"

# Create a text generation pipeline which use the model and the tokenizer loaded
generator = pipeline(task="text-classification", model=model, tokenizer=tokenizer)

# Identify Product Architecture Statements
##########################################
##########################################
#             Work Here
##########################################
##########################################
import textwrap

def display_response(prompt, generated_response, max_width=120):
    # Function to print a bordered text box
    def print_boxed(text):
        lines = textwrap.wrap(text, max_width)  # Wrap text to desired width
        border = '+' + '-' * (max_width + 2) + '+'
        print(border)
        for line in lines:
            print('| ' + line.ljust(max_width) + ' |')
        print(border)

    # Extract the instruction and the patient's query from the prompt
    instruction_start = prompt.find("[INST]") + len("[INST]")
    instruction_end = prompt.find("[/INST]")
    instruction = prompt[instruction_start:instruction_end].strip()

    prefix = "Search text and list all cause and effect statements about product architecture: "
    if instruction.startswith(prefix):
        instruction = instruction[len(prefix):].strip()

    # Extract the generated text from the response dictionary
    response_text = generated_response[0]['generated_text']

    # Extract the response from the generated text
    PA_statments_start = response_text.find("[/INST]") + len("[/INST]")
    PA_statements = response_text[PA_statments_start:].strip()

    # Display the information with a wrapper
    print("\nProduct Architecture Statements:")
    print_boxed(PA_statements)


prompt = """<s>[INST] Modularity makes development faster...  [/INST] """
outputs = generator(prompt)
print(outputs)

display_response(prompt, generator(prompt, max_new_tokens=100))

# Loading & Preprocessing Dataset
def template_dataset(sample):
    """
    Template a dataset sample to add a prompt to each sample for a patient-doctor interaction.

    Args:
        sample (dict): A dictionary containing 'Patient' and 'Doctor' fields which need to be templated.

    Returns:
        dict: The same dictionary but with an added 'text' field that contains the templated string.
    """

    cleaned_response = sample['Doctor'].replace('<start>', '').replace('<end>', '').strip()

    instruction = f"<s>[INST] As a medical doctor, respond to this patient query: Patient: {sample['Patient']} [/INST]"
    response = f"Doctor: {cleaned_response}"
    sample["text"] = instruction + response + tokenizer.eos_token
    return sample

# dataset_name: Identifies the name or path of the desired dataset.
dataset_name = 'sid6i7/patient-doctor'
dataset = load_dataset(dataset_name, split="train")
dataset_sample = 3000


if dataset_sample > 0:
  dataset_shuffled = dataset.shuffle(seed=1234)
  dataset = dataset_shuffled.select(range(dataset_sample))


dataset = dataset.map(template_dataset, remove_columns=[f for f in dataset.features if not f == 'text'])

new_model = 'Llama-7b-medical-assistance'

"""Select samples to check the datasets:"""

import random
idx_1 = random.randint(0, len(dataset))
idx_2 = random.randint(0, len(dataset))
idx_3 = random.randint(0, len(dataset))
idx_4 = random.randint(0, len(dataset))
idx_5 = random.randint(0, len(dataset))
print(f'Selected Samples for test: {idx_1}, {idx_2}, {idx_3}, {idx_4}, and {idx_5}')

print("="*50)
print("DATASET INFORMATION")
print("="*50)
print(f"Dataset Name: {dataset_name}\n")
print(f"Number of Samples: {len(dataset)}\n")

print("="*50)
print("RUNNING INFERENCE ON A SAMPLES")
print("="*50)
print(f"Sample Example (Index {idx_1}):")
prompt = f"{dataset[idx_1]['text'].split('[/INST]')[0]}[/INST] "
display_response(prompt, generator(prompt, max_new_tokens=200))
print("="*50)
print(f"Sample Example (Index {idx_2}):")
prompt = f"{dataset[idx_2]['text'].split('[/INST]')[0]}[/INST] "
display_response(prompt, generator(prompt, max_new_tokens=200))
print("="*50)
print(f"Sample Example (Index {idx_3}):")
prompt = f"{dataset[idx_3]['text'].split('[/INST]')[0]}[/INST] "
display_response(prompt, generator(prompt, max_new_tokens=200))
print("="*50)
print(f"Sample Example (Index {idx_4}):")
prompt = f"{dataset[idx_4]['text'].split('[/INST]')[0]}[/INST] "
display_response(prompt, generator(prompt, max_new_tokens=200))
print("="*50)
print(f"Sample Example (Index {idx_5}):")
prompt = f"{dataset[idx_5]['text'].split('[/INST]')[0]}[/INST] "
display_response(prompt, generator(prompt, max_new_tokens=200))
print("="*50)

print("MODEL INFORMATION")
print("="*50)
print(f"Fine-Tuned Model Name: {new_model}")
print("="*50)
