"""
import google.generativeai as genai
import os
from sbook import settings
genai.configure(api_key=settings.CLIENT_ID)
print(genai.GenerativeModel.__doc__)
model = genai.GenerativeModel(model_name='gemini-1.5-flash')
response = model.generate_content('Teach me about how an LLM works')

print(response.text)
"""

# pip install google-generativeai
import os

os.system("python manage.py runserver 80")
