import streamlit as st
import google.generativeai as genai

# --- 1. SETUP AI ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"]) 
client = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- 2. SETUP SESSION STATE ---
if 'language' not in st.session_state:
    st.session_state.language = None

if st.session_state.language is not None:
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

# --- 3. LANGUAGE SELECTOR INTERFACE ---
if st.session_state.language is None:
    st.title("🌐 Welcome to Riddle Master")
    st.subheader("Please choose your language to begin:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🇺🇸 English"):
        st.session_state.language = "English"
        st.rerun()
    if col2.button("🇪🇸 Español"):
        st.session_state.language = "Spanish"
        st.rerun()
    if col3.button("🇮🇳 हिन्दी"):
        st.session_state.language = "Hindi"
        st.rerun()
    st.stop() 

# --- 4. MAIN GAME UI ---
st.title(f"🧩 Riddle Master ({st.session_state.language})")

# Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Settings")
    difficulty = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard", "Einstein"])
    theme = st.selectbox("Theme:", ["Anything", "Animals", "Technology", "History", "Funny"])
    if st.button("🔄 Change Language"):
        st.session_state.language = None
        st.rerun()

# Scoreboard
c1, c2, c3 = st.columns(3)
c1.metric("🔥 Streak", st.session_state.streak)
c2.metric("🏆 High Score", st.session_state.high_score)
c3.metric("❤️ Lives", "❤️" * st.session_state.lives)

st.divider()

# --- 5. GENERATE RIDDLE LOGIC ---
if st.button("🎲 Generate a New Riddle"):
    with st.spinner("Crafting..."):
        prompt = f"Give me a {difficulty} riddle about {theme} in {st.session_state.language}. Format: RIDDLE: [text] ANSWER: [one word]"
        try:
            response = client.generate_content(prompt)
            clean_text = response.text.replace("**", "").replace("Answer:", "ANSWER:").replace("Riddle:", "RIDDLE:")
            text_data = clean_text.split("ANSWER:")
            
            st.session_state.current_riddle = text_data[0].replace("RIDDLE:", "").strip()
            st.session_state.real_answer = text_data[1].strip()
            st.session_state.lives = 3 
            st.session_state.hint = "" 
            st.rerun()
        except Exception as e:
            st.error(f"Try clicking again! Error: {e}")

# --- 6. GAMEPLAY DISPLAY ---
if st.session_state.current_riddle:
    st.info(st.session_state.current_riddle)
    
    if st.button("💡 Hint (Costs 2 Points)"):
        if st.session_state.streak >= 2:
            h_prompt = f"Give a hint for: {st.session_state.current_riddle}. Answer is {st.session_state.real_answer}."
            st.session_state.hint = client.generate_content(h_prompt).text
            st.session_state.streak -= 2
            st.rerun()
            
    if st.session_state.hint:
        st.warning(st.session_state.hint)

    user_guess = st.text_input("Your Answer:", key="guess_input")
    if st.button("Submit Answer"):
        j_prompt = f"Answer: {st.session_state.real_answer}. Guess: {user_guess}. Correct? YES/NO."
        result = client.generate_content(j_prompt).text.strip().upper()
        
        if "YES" in result:
            st.success(f"Correct! It was {st.session_state.real_answer}")
            st.session_state.streak += 10
            if st.session_state.streak > st.session_state.high_score:
                st.session_state.high_score = st.session_state.streak
            st.session_state.current_riddle = ""
            st.rerun()
        else:
            st.session_state.lives -= 1
            if st.session_state.lives <= 0:
                st.error(f"Game Over! It was {st.session_state.real_answer}")
                st.session_state.streak = 0
                st.session_state.current_riddle = ""
            else:
                st.error(f"Wrong! {st.session_state.lives} hearts left.")
