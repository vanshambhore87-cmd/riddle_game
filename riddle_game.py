import streamlit as st
import google.generativeai as genai
import time

# =========================================
# 1. PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Riddle Master",
    page_icon="🧩",
    layout="centered"
)

# =========================================
# 2. GEMINI SETUP
# =========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash-lite")

# =========================================
# 3. SESSION STATE
# =========================================
defaults = {
    "language": None,
    "streak": 0,
    "high_score": 0,
    "current_riddle": "",
    "real_answer": "",
    "lives": 3,
    "hint": "",
    "answered": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================
# 4. FUNCTIONS
# =========================================

def generate_riddle(difficulty, theme, language):
    """
    Generate a riddle using Gemini AI
    """

    prompt = f"""
Generate ONE unique {difficulty} riddle about {theme} in {language}.

STRICT RULES:
1. Keep riddle short.
2. Answer must be ONE WORD only.
3. Use EXACT format below.

RIDDLE: <riddle here>
ANSWER: <answer here>
"""

    response = model.generate_content(prompt)

    clean_text = response.text.strip()

    clean_text = (
        clean_text
        .replace("**", "")
        .replace("Answer:", "ANSWER:")
        .replace("Riddle:", "RIDDLE:")
    )

    if "ANSWER:" not in clean_text:
        return None, None

    parts = clean_text.split("ANSWER:")

    riddle = parts[0].replace("RIDDLE:", "").strip()
    answer = parts[1].strip()

    return riddle, answer


def generate_hint(riddle, answer, language):
    """
    Generate hint using Gemini
    """

    prompt = f"""
Give a SHORT hint in {language}.

Riddle: {riddle}
Answer: {answer}

Rules:
- Do not reveal the answer.
- Maximum 1 sentence.
"""

    response = model.generate_content(prompt)

    return response.text.strip()


# =========================================
# 5. LANGUAGE SELECTOR
# =========================================
if st.session_state.language is None:

    st.title("🧩 Riddle Master")
    st.subheader("Choose your language")

    c1, c2, c3 = st.columns(3)

    if c1.button("🇺🇸 English", use_container_width=True):
        st.session_state.language = "English"
        st.rerun()

    if c2.button("🇪🇸 Español", use_container_width=True):
        st.session_state.language = "Spanish"
        st.rerun()

    if c3.button("🇮🇳 हिन्दी", use_container_width=True):
        st.session_state.language = "Hindi"
        st.rerun()

    st.stop()

# =========================================
# 6. MAIN TITLE
# =========================================
st.title(f"🧩 Riddle Master ({st.session_state.language})")

# =========================================
# 7. SIDEBAR
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
# 8. SCOREBOARD
# =========================================
a, b, c = st.columns(3)

a.metric("🔥 Streak", st.session_state.streak)
b.metric("🏆 High Score", st.session_state.high_score)
c.metric("❤️ Lives", st.session_state.lives)

st.divider()

# =========================================
# 9. GENERATE NEW RIDDLE BUTTON
# =========================================
if st.button("🎲 Generate New Riddle", use_container_width=True):

    with st.spinner("Generating awesome riddle..."):

        try:

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
                st.session_state.answered = False

                st.rerun()

            else:
                st.error("AI returned invalid format. Try again.")

        except Exception as e:
            st.error(f"Error: {e}")

# =========================================
# 10. DISPLAY RIDDLE
# =========================================
if st.session_state.current_riddle:

    st.subheader("🧠 Your Riddle")

    st.info(st.session_state.current_riddle)

    # =====================================
    # HINT BUTTON
    # =====================================
    if st.button("💡 Get Hint (-2 points)"):

        if st.session_state.streak >= 2:

            with st.spinner("Thinking of a hint..."):

                hint = generate_hint(
                    st.session_state.current_riddle,
                    st.session_state.real_answer,
                    st.session_state.language
                )

                st.session_state.hint = hint
                st.session_state.streak -= 2

                st.rerun()

        else:
            st.warning("You need at least 2 streak points.")

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
        placeholder="Type your answer here..."
    )

    # =====================================
    # SUBMIT ANSWER
    # =====================================
    if st.button("✅ Submit Answer", use_container_width=True):

        correct_answer = st.session_state.real_answer.strip().lower()

        player_answer = user_guess.strip().lower()

        if player_answer == correct_answer:

            st.success(
                f"🎉 Correct! The answer was: "
                f"{st.session_state.real_answer}"
            )

            st.balloons()

            st.session_state.streak += 10

            if st.session_state.streak > st.session_state.high_score:

                st.session_state.high_score = st.session_state.streak

            st.session_state.answered = True

            time.sleep(2)

            st.session_state.current_riddle = ""
            st.session_state.real_answer = ""
            st.session_state.hint = ""

            st.rerun()

        else:

            st.session_state.lives -= 1

            if st.session_state.lives <= 0:

                st.error(
                    f"💀 Game Over! "
                    f"The answer was: {st.session_state.real_answer}"
                )

                st.session_state.streak = 0

                time.sleep(2)

                st.session_state.current_riddle = ""
                st.session_state.real_answer = ""
                st.session_state.hint = ""

                st.rerun()

            else:

                st.error(
                    f"❌ Wrong Answer! "
                    f"{st.session_state.lives} lives remaining."
                )

# =========================================
# 11. EMPTY STATE
# =========================================
else:

    st.markdown(
        """
        ## 👇 Start Playing
        
        Press **Generate New Riddle** to begin!
        """
    )