import streamlit as st
import google.generativeai as genai
import time
import random

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(page_title="Riddle Master", page_icon="🧩", layout="centered")

# =========================================
# GEMINI API SETUP
# =========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# =========================================
# SESSION STATE DEFAULTS (Now holding all settings!)
# =========================================
defaults = {
    "language": None,
    "streak": 0,
    "high_score": 0,
    "current_riddle": "",
    "real_answer": "",
    "lives": 3,
    "hint": "",
    "show_next": False,
    "status_msg": "", 
    "difficulty": "Easy", # Locked into core memory
    "theme": "Anything"   # Locked into core memory
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================
# FUNCTIONS
# =========================================
def generate_riddle(diff, thm, lang):
    prompt = f"""
Generate ONE highly unique {diff} difficulty riddle about {thm} in {lang}.
Make it completely different from standard riddles. (Seed: {random.randint(1, 100000)})

RULES:
1. Keep the riddle short.
2. Answer must be ONE WORD only.
3. Use EXACT format below.

RIDDLE: <riddle>
ANSWER: <answer>
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip().replace("**", "").replace("Riddle:", "RIDDLE:").replace("Answer:", "ANSWER:")

        if "ANSWER:" not in text:
            return None, None

        parts = text.split("ANSWER:")
        riddle = parts[0].replace("RIDDLE:", "").strip()
        answer = parts[1].strip()
        return riddle, answer
    except:
        return None, None

def generate_hint(riddle, answer, lang):
    prompt = f"Give a SHORT hint in {lang}. \nRiddle: {riddle}\nAnswer: {answer}\nRules: Do not reveal answer, Max one sentence."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "Hint system is currently cooling down!"

def load_new_riddle(diff, thm, lang):
    riddle, answer = generate_riddle(diff, thm, lang)
    if riddle and answer:
        st.session_state.current_riddle = riddle
        st.session_state.real_answer = answer
        st.session_state.hint = ""
        st.session_state.lives = 3
        st.session_state.show_next = False
        st.session_state.status_msg = "" 
    else:
        st.session_state.current_riddle = "⚠️ The AI got confused! Please click the 'Force New Riddle' button above."
        st.session_state.show_next = False

# =========================================
# LANGUAGE SELECTOR
# =========================================
if st.session_state.language is None:
    st.title("🧩 Riddle Master")
    st.subheader("Choose your language")
    c1, c2, c3 = st.columns(3)
    if c1.button("🇺🇸 English", use_container_width=True):
        st.session_state.language = "English"
        st.rerun()
    if c2.button("🧡 मराठी", use_container_width=True):
        st.session_state.language = "Marathi"
        st.rerun()
    if c3.button("🇮🇳 हिन्दी", use_container_width=True):
        st.session_state.language = "Hindi"
        st.rerun()
    st.stop()

# =========================================
# UI HEADER & SIDEBAR
# =========================================
st.title(f"🧩 Riddle Master ({st.session_state.language})")

with st.sidebar:
    st.header("⚙️ Settings")
    # Added "key=" to link dropdowns directly to core memory
    st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Einstein"], key="difficulty")
    st.selectbox("Theme", ["Anything", "Animals", "Technology", "History", "Funny"], key="theme")
    st.divider()
    if st.button("🌐 Change Language", use_container_width=True):
        for key, value in defaults.items():
            st.session_state[key] = value
        st.rerun()

# SKIP BUTTON 
if st.button("🔄 Force New Riddle", use_container_width=True):
    st.session_state.current_riddle = ""
    st.session_state.show_next = False 
    st.rerun()

# SCOREBOARD
a, b, c = st.columns(3)
a.metric("🔥 Streak", st.session_state.streak)
b.metric("🏆 High Score", st.session_state.high_score)
c.metric("❤️ Lives", st.session_state.lives)
st.divider()

# =========================================
# GAMEPLAY ENGINE 
# =========================================
if st.session_state.current_riddle == "":
    with st.spinner("Generating unique riddle..."):
        # THE FIX: Calling difficulty and theme directly from Core Memory
        load_new_riddle(st.session_state.difficulty, st.session_state.theme, st.session_state.language)

if st.session_state.current_riddle:
    st.subheader("🧠 Your Riddle")
    st.info(st.session_state.current_riddle)

    if st.button("💡 Get Hint (-2 points)"):
        if st.session_state.streak >= 2:
            with st.spinner("Generating hint..."):
                st.session_state.hint = generate_hint(st.session_state.current_riddle, st.session_state.real_answer, st.session_state.language)
                st.session_state.streak -= 2
                st.rerun()
        else:
            st.warning("Need at least 2 points!")
            
    if st.session_state.hint:
        st.warning(f"💡 Hint: {st.session_state.hint}")

    if st.session_state.status_msg:
        if "Correct" in st.session_state.status_msg:
            st.success(st.session_state.status_msg)
        elif "Wrong" in st.session_state.status_msg:
            st.warning(st.session_state.status_msg)
        else:
            st.error(st.session_state.status_msg)

    # Input Form 
    if not st.session_state.show_next and "⚠️" not in st.session_state.current_riddle:
        with st.form("guess_form"):
            user_guess = st.text_input("Your Answer", placeholder="Type answer here...")
            submitted = st.form_submit_button("✅ Submit Answer", use_container_width=True)

            if submitted:
                correct_answer = st.session_state.real_answer.strip().lower()
                player_answer = user_guess.strip().lower()

                if player_answer == correct_answer:
                    st.session_state.status_msg = f"🎉 Correct! Answer was: {st.session_state.real_answer}"
                    st.session_state.streak += 10
                    if st.session_state.streak > st.session_state.high_score:
                        st.session_state.high_score = st.session_state.streak
                    st.session_state.show_next = True
                else:
                    st.session_state.lives -= 1
                    if st.session_state.lives <= 0:
                        st.session_state.status_msg = f"💀 Game Over! Answer was: {st.session_state.real_answer}"
                        st.session_state.streak = 0
                        st.session_state.show_next = True
                    else:
                        st.session_state.status_msg = f"❌ Wrong! {st.session_state.lives} lives left."
                
                st.rerun()

    # Next Button Layer
    if st.session_state.show_next:
        st.markdown("---")
        if st.button("➡️ GET NEXT RIDDLE", use_container_width=True, type="primary"):
            st.session_state.current_riddle = ""
            st.session_state.status_msg = ""
            st.session_state.show_next = False 
            st.rerun()
