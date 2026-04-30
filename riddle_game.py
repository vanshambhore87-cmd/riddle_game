import streamlit as st
import google.generativeai as genai

# --- 1. SETUP AI ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"]) 
client = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. SETUP SESSION STATE (The Brain) ---
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0
if 'current_riddle' not in st.session_state:
    st.session_state.current_riddle = ""
if 'real_answer' not in st.session_state:
    st.session_state.real_answer = ""
if 'lives' not in st.session_state:
    st.session_state.lives = 3
if 'hint' not in st.session_state:
    st.session_state.hint = ""

# --- 3. UI DESIGN & SIDEBAR ---
st.set_page_config(page_title="AI Riddle Master", page_icon="🧩")

# Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Game Settings")
    difficulty = st.selectbox("Choose Difficulty:", ["Easy", "Medium", "Hard", "Einstein Level"])
    theme = st.selectbox("Choose Theme:", ["Anything", "Animals", "Science", "Scary/Horror", "Video Games", "Funny"])
    st.markdown("---")
    st.write("💡 *Hints cost 2 points!*")

st.title("🧩 The Infinite Riddle Master V2")

# Scoreboard
col1, col2, col3 = st.columns(3)
col1.metric("🔥 Streak", st.session_state.streak)
col2.metric("🏆 High Score", st.session_state.high_score)
col3.metric("❤️ Lives", "❤️" * st.session_state.lives)

st.divider()

# --- 4. GAME LOOP ---

# Button to Generate Riddle
if st.button("🎲 Generate a New Riddle"):
    with st.spinner(f"The AI is crafting a {difficulty} {theme} riddle..."):
        prompt = f"Give me a {difficulty} difficulty riddle about {theme}. Format EXACTLY like this: \nRIDDLE: [riddle here] \nANSWER: [one word answer]"
        response = client.generate_content(prompt)
        
        try:
            text_data = response.text.split("ANSWER:")
            st.session_state.current_riddle = text_data[0].replace("RIDDLE:", "").strip()
            st.session_state.real_answer = text_data[1].strip()
            st.session_state.lives = 3 # Reset lives for new riddle
            st.session_state.hint = "" # Clear old hints
            st.rerun()
        except:
            st.error("AI got confused. Click generate again!")

# Display Riddle & Gameplay
if st.session_state.current_riddle:
    st.subheader("The Riddle:")
    st.info(st.session_state.current_riddle)
    
    # Hint System
    if st.button("💡 Ask AI for a Hint (Costs 2 Points)"):
        if st.session_state.streak >= 2:
            with st.spinner("AI is thinking of a hint..."):
                hint_prompt = f"The riddle is: '{st.session_state.current_riddle}' and the answer is '{st.session_state.real_answer}'. Give a short 1-sentence clue without revealing the exact answer."
                hint_response = client.generate_content(hint_prompt)
                st.session_state.hint = hint_response.text
                st.session_state.streak -= 2 # Deduct points
                st.rerun()
        else:
            st.warning("You need at least 2 points to buy a hint!")
            
    if st.session_state.hint:
        st.warning(f"**HINT:** {st.session_state.hint}")

    st.markdown("---")
    
    # Guessing System
    user_guess = st.text_input("Your Answer:")
    
    if st.button("Submit Answer"):
        with st.spinner("The Smart Judge is checking..."):
            judge_prompt = f"The real answer is '{st.session_state.real_answer}'. The user guessed '{user_guess}'. Are they basically correct? Reply with only YES or NO."
            judge_response = client.generate_content(judge_prompt).text.strip().upper()
            
            if "YES" in judge_response:
                st.success(f"CORRECT! The answer was: {st.session_state.real_answer}")
                st.session_state.streak += 10
                if st.session_state.streak > st.session_state.high_score:
                    st.session_state.high_score = st.session_state.streak
                st.session_state.current_riddle = "" 
                st.button("Next Riddle ➡️")
            else:
                st.session_state.lives -= 1
                if st.session_state.lives > 0:
                    st.error(f"WRONG! You lost a life. {st.session_state.lives} ❤️ remaining.")
                else:
                    st.error(f"GAME OVER! You lost all your lives. The correct answer was: {st.session_state.real_answer}")
                    st.session_state.streak = 0
                    st.session_state.current_riddle = ""
                    st.button("Start Over 🔄")