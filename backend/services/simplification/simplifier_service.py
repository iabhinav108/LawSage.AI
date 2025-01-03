import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("MikaSie/LegalBERT_BART_fixed_V1")
model = AutoModelForSeq2SeqLM.from_pretrained("MikaSie/LegalBERT_BART_fixed_V1")

model.to(device)

def simplify_summary(text, chunk_size=1024, min_length=100, max_length=200):
    
    inputs = tokenizer(text, return_tensors="pt", truncation=False)
    input_ids = inputs["input_ids"]

    chunks = [input_ids[0][i:i + chunk_size] for i in range(0, input_ids.size(1), chunk_size)]
    simplified_chunks = []

    for chunk in chunks:
        chunk_inputs = {"input_ids": chunk.unsqueeze(0).to(device)}
        outputs = model.generate(
            chunk_inputs["input_ids"],
            max_length=max_length,
            num_beams=4,
            min_length=min_length,
            length_penalty=1.0,
            no_repeat_ngram_size=3
        )
        simplified_chunk = tokenizer.decode(outputs[0], skip_special_tokens=True)
        simplified_chunks.append(simplified_chunk)
    
    simplified_summary = " ".join(simplified_chunks)
    return simplified_summary
