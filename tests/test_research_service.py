from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3.5-mini-instruct")
model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3.5-mini-instruct")
legal_assistant = pipeline("text-generation", model=model, tokenizer=tokenizer)

print("Pipeline initialized successfully.")
