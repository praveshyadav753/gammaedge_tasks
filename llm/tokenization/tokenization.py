from transformers import BertTokenizer

tokenizer =BertTokenizer.from_pretrained('bert-base-uncased')
token =tokenizer.tokenize("what is the meaning of tokenization and how it works?")
# sub word tokenization
print("subword",token)


import tiktoken

enc = tiktoken.get_encoding("gpt2")

token_ids = enc.encode("this is byte pair encoding tokenization used by chatgpt which is a subword tokanization, .")
print(f"Token IDs: {token_ids}")
decoded_text = enc.decode(token_ids)
print(f"Decoded text: {decoded_text}")
