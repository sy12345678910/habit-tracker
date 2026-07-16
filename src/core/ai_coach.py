import time
from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv(override=True)

def get_ai_advice(habit_list):
    client = genai.Client()
    
    prompt = (
        "You are Angry AI, a tough, charismatic and very sarcastic AI coach. "
        "Your goal is to analyze my habits and give me short but biting criticism or motivation with a little black humor. "
        "Don't praise me for zeros! Scold me for failures, but ironically support me if I make any progress. "
        "Answer in English.\n\n"
        "Here is my list of habits:\n"
    )
    
    for i in habit_list:
        prompt += f"- {i['title']}: current strike {i['current_strike']}, record {i['max_strike']}\n" 
        
    for attempt in range(3):
        try:    
            response = client.models.generate_content(
                model='gemini-3.5-flash', 
                contents=prompt,
            )
            return response.text
        except errors.APIError as e:
            if e.code == 503 and attempt < 2:
                time.sleep(2)
                continue
            
            raise e