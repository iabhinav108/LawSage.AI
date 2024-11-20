import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("nsi319/legal-pegasus")
model = AutoModelForSeq2SeqLM.from_pretrained("nsi319/legal-pegasus")
model = model.to(device)

def chunk_text(text, tokenizer, max_length=1024):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    
    chunks = []
    for start in range(0, len(tokens), max_length - 200):
        chunk_tokens = tokens[start:start + max_length]
        chunk = tokenizer.decode(chunk_tokens)
        chunks.append(chunk)
    
    return chunks

def summarize_long_text(text, tokenizer, model, max_chunk_length=1024):
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    chunks = chunk_text(text, tokenizer, max_chunk_length)
    
    chunk_summaries = []
    for chunk in chunks:
        input_tokenized = tokenizer.encode(chunk, return_tensors='pt', 
                                           max_length=max_chunk_length,
                                           truncation=True).to(device)
        
        summary_ids = model.generate(input_tokenized,
                                     num_beams=9,
                                     no_repeat_ngram_size=3,
                                     length_penalty=2.0,
                                     min_length=50,
                                     max_length=300,
                                     early_stopping=False,
                                     do_sample=True,
                                     top_k=50,
                                     top_p=0.95) 
        
        summary = tokenizer.decode(summary_ids[0], 
                                   skip_special_tokens=True, 
                                   clean_up_tokenization_spaces=False)
        chunk_summaries.append(summary)
    
    combined_summary = " ".join(chunk_summaries)
    final_input = tokenizer.encode(combined_summary, 
                                   return_tensors='pt', 
                                   max_length=max_chunk_length,
                                   truncation=True).to(device)
    
    final_summary_ids = model.generate(final_input,
                                       num_beams=9,
                                       no_repeat_ngram_size=3,
                                       length_penalty=2.0,
                                       min_length=100,
                                       max_length=500,
                                       early_stopping=False,
                                       do_sample=True,
                                       top_k=50,
                                       top_p=0.95)
    
    final_summary = tokenizer.decode(final_summary_ids[0], 
                                     skip_special_tokens=True, 
                                     clean_up_tokenization_spaces=False)
    
    return final_summary

def summarize_text(text, min_length=150, max_length=250):
    if not text or len(text.strip()) == 0:
        print("Input text is empty or only whitespace.")
        return "Input text is empty or only whitespace."
    
    return summarize_long_text(text, tokenizer, model)

