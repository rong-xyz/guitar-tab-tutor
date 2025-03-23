# explanation.py
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_guitar_explanation(question, user_answer, true_answer):
    """
    Generate an explanation for music theory answers focusing on guitar application.
    
    Args:
        question (str): The original music theory question
        user_answer (str): The answer provided by the user
        true_answer (str): The correct answer
        
    Returns:
        str: Guitar-focused explanation for finding this note on the fretboard
    """
    # Construct a prompt for OpenAI that will generate guitar-specific explanations
    prompt = f"""
    You are a guitar and music theory teacher. Explain the following music theory question and answer 
    in terms of guitar fretboard positions. 

    Question: {question}
    User's answer: {user_answer}
    Correct answer: {true_answer}
    
    Please provide a brief explanation (around 100-150 words) focusing on:
    1. Where to find this note on a standard-tuned guitar
    2. How to derive this note using the relationship between strings(Eg use power chord relation ship to find root/fifth then go up down)
    3. How understanding this helps with playing and improvisation
    4. Include specific fret positions (e.g., "5th string 3rd fret is C")
    
    Make your explanation practical for a guitarist who's learning music theory and answer in Chinese
    """
    
    try:
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o",  # You can use "gpt-4" for more advanced responses if available
            messages=[
                {"role": "system", "content": "You are a helpful guitar teacher who explains music theory in practical terms."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.7
        )
        
        # Extract and return the explanation
        explanation = response.choices[0].message.content
        return explanation
    
    except Exception as e:
        # Return a basic explanation if API fails
        return f"Error generating explanation: {str(e)}"