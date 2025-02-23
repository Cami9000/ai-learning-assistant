import streamlit as st
import requests

# FlowiseAI API URL
FLOWISE_API_URL = "http://localhost:3000/api/v1/prediction/8d99063c-b692-4863-a818-0a080bbb012d"

def get_ai_response(topic):
    """Sends a request to FlowiseAI to get an explanation and a quiz."""
    prompt = f"Explain {topic} in simple terms and create a quiz with 3 questions."
    
    try:
        response = requests.post(FLOWISE_API_URL, json={"question": prompt})
        response_data = response.json()
        
        # Debugging: Print API response to terminal
        print("API Response:", response_data)
        
        if response.status_code == 200:
            full_text = response_data.get("text", "Error: No response text from AI.")
            
            # Split into explanation and quiz
            explanation, quiz = full_text.split("Quiz:\n", 1) if "Quiz:\n" in full_text else (full_text, "No quiz found.")
            return explanation.strip(), quiz.strip()
        else:
            return f"Error: {response.status_code} - {response_data}", "No quiz found."
    
    except Exception as e:
        return f"Request failed: {e}", "No quiz found."

# Streamlit UI
st.title("📚 AI Learning Assistant")
st.write("Learn a new topic with AI! Choose a topic and get an explanation and a quiz.")

# User input
topic = st.text_input("Enter a topic you want to learn about:")

if st.button("Learn now!"):
    if topic:
        with st.spinner("AI is thinking..."):
            explanation, quiz = get_ai_response(topic)
        
        # Display explanation
        st.subheader("📖 Explanation")
        st.write(explanation)
        
        # Display quiz
        st.subheader("📝 Quiz")
        st.write(quiz)
    else:
        st.warning("Please enter a topic first!")
