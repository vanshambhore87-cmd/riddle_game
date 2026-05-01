import streamlit as st
import google.generativeai as genai
import time

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Riddle Master",
    page_icon="🧩",
    layout="centered"
)

# =========================================
# GEMINI API SETUP
# =========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash-lite")

# =========================================
# SESSION STATE DEFAULTS
# =========================================
defaults = {
    "language": None,
    "streak": 0,
    "high_score": 0,
    "current_riddle": "",
    "real_answer": "",
    "lives": 3,
    "hint": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================
# FUNCTIONS
# =========================================

def generate_riddle(difficulty, theme, language):
    prompt = f"""
Generate ONE unique {difficulty} riddle about {theme} in {language}.

RULES:
1. Keep the riddle short.
2. Answer must be ONE WORD only.
3. Use EXACT format below.

RIDDLE: <riddle>
ANSWER: <answer>
"""
    response = model.generate_content(prompt)
    text = response.text.strip()
    text = (
        text.replace("**", "")
        .replace("Riddle:", "RIDDLE:")
        .replace("Answer:", "ANSWER:")
    )

    if "ANSWER:" not in text:
        return None, None

    parts = text.split("ANSWER:")
    riddle = parts[0].replace("RIDDLE:", "").strip()
    answer = parts[1].strip()

    return riddle, answer


def generate_hint(riddle, answer, language):
    prompt = f"""
Give a SHORT hint in {language}.

Riddle: {riddle}
Answer: {answer}

Rules:
- Do not reveal answer
- Maximum one sentence
"""
    response = model.generate_content(prompt)
    return response.text.strip()


def load_new_riddle():
    riddle, answer = generate_riddle(
        difficulty,
        theme,
        st.session_state.language
    )
    if riddle and answer:
        st.session_state.current_riddle = riddle
        st.session_state.real_answer = answer
        st.session_state.hint = ""
        st.session_state.lives = 3


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

    if c2.button("🧡 मराठी ", use_container_width=True):
        st.session_state.language = "Marathi"
        st.rerun()

    if c3.button("🇮🇳 हिन्दी", use_container_width=True):
        st.session_state.language = "Hindi"
        st.rerun()

    st.stop()

# =========================================
# MAIN TITLE
# =========================================
st.title(f"🧩 Riddle Master ({st.session_state.language})")

# =========================================
# SIDEBAR
# =========================================
with st.sidebar:
    st.header("⚙️ Settings")

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard", "Einstein"]
    )

    theme = st.selectbox(
        "Theme",
        ["Anything", "Animals", "Technology", "History", "Funny"]
    )

    st.divider()

    if st.button("🌐 Change Language", use_container_width=True):
        for key, value in defaults.items():
            st.session_state[key] = value
        st.rerun()

# =========================================
# NEW SKIP / FORCE NEW RIDDLE BUTTON
# =========================================
if st.button("⏭️ Skip / Force New Riddle", use_container_width=True):
    st.session_state.current_riddle = ""
    st.rerun()

# =========================================
# SCOREBOARD
# =========================================
a, b, c = st.columns(3)

a.metric("🔥 Streak", st.session_state.streak)
b.metric("🏆 High Score", st.session_state.high_score)
c.metric("❤️ Lives", st.session_state.lives)

st.divider()

# =========================================
# AUTO LOAD FIRST RIDDLE
# =========================================
if st.session_state.current_riddle == "":
    with st.spinner("Generating riddle..."):
        load_new_riddle()

# =========================================
# DISPLAY RIDDLE
# =========================================
if st.session_state.current_riddle:
    st.subheader("🧠 Your Riddle")
    st.info(st.session_state.current_riddle)

    # =====================================
    # HINT BUTTON
    # =====================================
    if st.button("💡 Get Hint (-2 points)"):
        if st.session_state.streak >= 2:
            with st.spinner("Generating hint..."):
                hint = generate_hint(
                    st.session_state.current_riddle,
                    st.session_state.real_answer,
                    st.session_state.language
                )
                st.session_state.hint = hint
                st.session_state.streak -= 2
                st.rerun()
        else:
            st.warning("Need at least 2 points!")

    # =====================================
    # SHOW HINT
    # =====================================
    if st.session_state.hint:
        st.warning(f"💡 Hint: {st.session_state.hint}")

    # =====================================
    # ANSWER INPUT
    # =====================================
    user_guess = st.text_input(
        "Your Answer",
        placeholder="Type answer here..."
    )

    # =====================================
    # SUBMIT BUTTON
    # =====================================
    if st.button("✅ Submit Answer", use_container_width=True):
        correct_answer = st.session_state.real_answer.strip().lower()
        player_answer = user_guess.strip().lower()

        if player_answer == correct_answer:
            st.success(f"🎉 Correct! Answer was: {st.session_state.real_answer}")
            st.balloons()
            st.session_state.streak += 10

            if st.session_state.streak > st.session_state.high_score:
                st.session_state.high_score = st.session_state.streak

            time.sleep(2)

            # AUTO LOAD NEXT RIDDLE
            st.session_state.current_riddle = "" # Wipe the old riddle to trigger a new one
            st.rerun()

        else:
            st.session_state.lives -= 1

            if st.session_state.lives <= 0:
                st.error(f"💀 Game Over! Answer was: {st.session_state.real_answer}")
                st.session_state.streak = 0
                time.sleep(2)
                
                # AUTO LOAD NEW RIDDLE
                st.session_state.current_riddle = ""
                st.rerun()
            else:
                st.error(f"❌ Wrong! {st.session_state.lives} lives left.")
