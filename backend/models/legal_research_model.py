import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import gc
import logging
import re

logging.basicConfig(level=logging.INFO)

device = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Using device: {device}")

tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/Phi-3.5-mini-instruct",
    truncation=True
)

try:
    model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Phi-3.5-mini-instruct",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    model = None

legal_assistant = None

try:
    if model:
        legal_assistant = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer
        )
        logging.info("Pipeline created successfully.")
except Exception as e:
    logging.error(f"Error creating pipeline: {e}")

def determine_max_tokens(prompt):
    num_words = len(prompt.split())
    max_tokens = min(1000, max(150, 3 * num_words))
    return max_tokens

def is_sentence_complete(text):
    return bool(re.search(r'[.!?]["\']?\s*$', text))

def ask_legal_question(prompt):
    logging.info(f"Received prompt: {prompt}")
    
    max_new_tokens = determine_max_tokens(prompt)

    if not legal_assistant:
        logging.error("Pipeline is not initialized. Cannot generate response.")
        return "An error occurred while generating the response."

    try:
        response = legal_assistant(
            prompt,
            num_return_sequences=1,
            max_new_tokens=max_new_tokens,
            eos_token_id=tokenizer.eos_token_id
        )
        generated_text = response[0]['generated_text']

        while not is_sentence_complete(generated_text) and len(generated_text.split()) < max_new_tokens:
            additional_response = legal_assistant(
                generated_text,
                num_return_sequences=1,
                max_new_tokens=50,
                eos_token_id=tokenizer.eos_token_id
            )
            new_text = additional_response[0]['generated_text']
            generated_text = new_text if len(new_text) > len(generated_text) else generated_text

        logging.info(f"Generated response: {generated_text}")
        return generated_text
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return "An error occurred while generating the response."

torch.cuda.empty_cache()
gc.collect()
