
from google import genai
from dotenv import load_dotenv
import os 

api_key = os.getenv('OPEN_API')

if api_key:
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents="write story on cow standing near pond",
            config=genai.types.GenerateContentConfig(
                temperature=0.3,
                top_p=0.8,
                # top_k=700,
                # seed=120,
                max_output_tokens=10000,
                # presence_penalty =0.3,
                # frequency_penalty=1,
                # candidate_count =2,

            ),
        )
        print(response)
        print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("API key not found. Please set the GEMINI_API_KEY environment variable.")

