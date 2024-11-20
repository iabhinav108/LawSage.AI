# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# # Load the tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained("nsi319/legal-pegasus")
# model = AutoModelForSeq2SeqLM.from_pretrained("nsi319/legal-pegasus")

# def summarize_text(text, min_length=150, max_length=250):
#     # Tokenize the input text
#     input_tokenized = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)
    
#     # Generate the summary
#     summary_ids = model.generate(
#         input_tokenized,
#         num_beams=9,
#         no_repeat_ngram_size=3,
#         length_penalty=2.0,
#         min_length=min_length,
#         max_length=max_length,
#         early_stopping=True
#     )
    
#     # Decode the generated summary
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
#     return summary

# # Example usage
# text = """On March 5, 2021, the Securities and Exchange Commission charged AT&T, Inc. with repeatedly violating 
# Regulation FD, and three of its Investor Relations executives with aiding and abetting AT&T's violations, by 
# selectively disclosing material nonpublic information to research analysts. According to the SEC's complaint, AT&T 
# learned in March 2016 that a steeper-than-expected decline in its first quarter smartphone sales would cause AT&T's 
# revenue to fall short of analysts' estimates for the quarter. The complaint alleges that to avoid falling short of the 
# consensus revenue estimate for the third consecutive quarter, AT&T Investor Relations executives Christopher Womack, 
# Michael Black, and Kent Evans made private, one-on-one phone calls to analysts at approximately 20 separate firms. 
# On these calls, the AT&T executives allegedly disclosed AT&T's internal smartphone sales data and the impact of that 
# data on internal revenue metrics, despite the fact that internal documents specifically informed Investor Relations 
# personnel that AT&T's revenue and sales of smartphones were types of information generally considered 'material' to 
# AT&T investors, and therefore prohibited from selective disclosure under Regulation FD. The complaint further alleges 
# that as a result of what they were told on these calls, the analysts substantially reduced their revenue forecasts, 
# leading to the overall consensus revenue estimate falling to just below the level that AT&T ultimately reported to 
# the public on April 26, 2016. The SEC's complaint, filed in federal district court in Manhattan, charges AT&T with 
# violations of the disclosure provisions of Section 13(a) of the Securities Exchange Act of 1934 and Regulation FD 
# thereunder, and charges Womack, Evans and Black with aiding and abetting these violations. The complaint seeks 
# permanent injunctive relief and civil monetary penalties against each defendant. The SEC's investigation was conducted 
# by George N. Stepaniuk, Thomas Peirce, and David Zetlin-Jones of the SEC's New York Regional Office. The SEC's 
# litigation will be conducted by Alexander M. Vasilescu, Victor Suthammanont, and Mr. Zetlin-Jones. The case is being 
# supervised by Sanjay Wadhwa."""

# # Get the summary
# summary = summarize_text(text)
# print("Summary:")
# print(summary)




# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
# import gc
# import logging

# # Initialize logging to help debug and track the application
# logging.basicConfig(level=logging.INFO)

# # Determine the device (GPU or CPU)
# device = "cuda" if torch.cuda.is_available() else "cpu"
# logging.info(f"Using device: {device}")

# # Load the tokenizer with explicit truncation
# tokenizer = AutoTokenizer.from_pretrained(
#     "microsoft/Phi-3.5-mini-instruct",
#     truncation=True  # Enable truncation to avoid exceeding model limits
# )

# # Load the model with FP16 precision, automatically mapping to GPU or CPU
# try:
#     model = AutoModelForCausalLM.from_pretrained(
#         "microsoft/Phi-3.5-mini-instruct",
#         torch_dtype=torch.float16,  # Use FP16 to reduce memory usage
#         device_map="auto"  # Automatically handles device allocation
#     )
#     logging.info("Model loaded successfully.")
# except Exception as e:
#     logging.error(f"Error loading model: {e}")

# # Create the text-generation pipeline without specifying the device explicitly
# try:
#     legal_assistant = pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer
#     )
#     logging.info("Pipeline created successfully.")
# except Exception as e:
#     logging.error(f"Error creating pipeline: {e}")

# # Function to handle legal question prompts
# def ask_legal_question(prompt, max_new_tokens=300):
#     logging.info(f"Received prompt: {prompt}")
#     try:
#         response = legal_assistant(
#             prompt,
#             num_return_sequences=1,
#             max_new_tokens=max_new_tokens
#         )
#         generated_text = response[0]['generated_text']
#         logging.info(f"Generated response: {generated_text}")
#         return generated_text
#     except Exception as e:
#         logging.error(f"Error generating response: {e}")
#         return "An error occurred while generating the response."

# # Clear CUDA cache and collect garbage to free memory
# torch.cuda.empty_cache()
# gc.collect()

# # Test function outside of Flask (Optional)
# if __name__ == "__main__":
#     # Example prompt to test outside of Flask
#     prompt = "Fundamental rights of Indian Constitution?"
#     print(ask_legal_question(prompt, max_new_tokens=300))



import os
secret_key = os.urandom(24).hex()
print(secret_key)
