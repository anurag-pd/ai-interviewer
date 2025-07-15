
# Use Groq API instead of OpenAI
import groq

# Create a Groq client (API key is automatically read from env var GROQ_API_KEY)
client = groq.Groq(api_key='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')

def generate_followup(user_response: str, difficulty: str = "medium") -> str:
    prompt = f"""You are a helpful AI technical interviewer.
            The candidate just answered:
            \"\"\"{user_response}\"\"\"

            Ask a short and relevant technical follow-up question.
            Keep it precise, direct, and avoid repeating the candidate's answer.
            Make the question {difficulty} difficulty. Just return the question text without any additional commentary."""

    try:
        response = client.chat.completions.create(
            model="compound-beta",
            messages=[
                {"role": "system", "content": "You are a technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100,
        )
        # Defensive: ensure response structure is correct
        if response and hasattr(response, 'choices') and response.choices:
            content = getattr(response.choices[0].message, 'content', None)
            if content:
                return content.strip()
        return "Thanks! Can you elaborate more on that?"

    except Exception as e:
        print(f"Error generating follow-up question: {e}")
        return "Thanks! Can you elaborate more on that?"
