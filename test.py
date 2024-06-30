from transformers import pipeline

# download & load GPT-2 model
gpt2_generator = pipeline('text-generation', model='gpt2')

# generate 3 different sentences
# results are sampled from the top 50 candidates
sentences = gpt2_generator("To be honest, neural networks", do_sample=True, top_k=50, temperature=0.6, max_length=128, num_return_sequences=3)
for sentence in sentences:
    print(sentence["generated_text"])
    print("="*50)
