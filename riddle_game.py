import streamlit as st
import google.generativeai as genai
import random

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Riddle Master",
    page_icon="🧩",
    layout="centered"
)

# =========================================
# GEMINI SETUP
# =========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash-lite")

# =========================================
# SESSION STATE
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
    "difficulty": "Easy",
    "theme": "Anything"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================
# FUNCTIONS
# =========================================
def generate_riddle(diff, thm, lang):

    prompt = f"""
Generate ONE {diff} riddle about {thm} in {lang}.

RULES:
- Keep it short
- Answer must be ONE WORD only
- Do not explain answer

FORMAT:
RIDDLE: question here
ANSWER: answer here
"""

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        text = text.replace("**", "")

        lines = text.splitlines()

        riddle = ""
        answer = ""

        for line in lines:

            line = line.strip()

            upper = line.upper()

            if upper.startswith("RIDDLE"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    riddle = parts[1].strip()

            elif upper.startswith("ANSWER"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    answer = parts[1].strip()

        # FALLBACK
        if riddle == "" or answer == "":

            clean_lines = [
                l.strip() for l in lines if l.strip()
            ]

            if len(clean_lines) >= 2:
                riddle = clean_lines[0]
                answer = clean_lines[-1]

        if riddle and answer:
            return riddle, answer

        return None, None

    except Exception as e:

        st.error(f"AI Error: {e}")

        return None, None


def generate_hint(riddle, answer, lang):

    prompt = f"""
Give ONE short hint in {lang}.

Riddle: {riddle}
Answer: {answer}

Do not reveal answer.
"""

    try:

        response = model.generate_content(prompt)

        return response.text.strip()

    except:

        return "Hint unavailable."


def load_new_riddle():

    riddle, answer = generate_riddle(
        st.session_state.difficulty,
        st.session_state.theme,
        st.session_state.language
    )

    if riddle and answer:

        st.session_state.current_riddle = riddle
        st.session_state.real_answer = answer
        st.session_state.hint = ""
        st.session_state.status_msg = ""
        st.session_state.show_next = False
        st.session_state.lives = 3

    else:

        st.session_state.current_riddle = ""
        st.session_state.real_answer = ""

        st.session_state.status_msg = (
            "⚠️ AI failed to generate riddle. "
            "Click below to try again."
        )


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
# TITLE
# =========================================
st.title(f"🧩 Riddle Master ({st.session_state.language})")

# =========================================
# SIDEBAR
# =========================================
with st.sidebar:

    st.header("⚙️ Settings")

    st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard", "Einstein"],
        key="difficulty"
    )

    st.selectbox(
        "Theme",
        [
            "Anything",
            "Animals",
            "Technology",
            "History",
            "Funny"
        ],
        key="theme"
    )

    st.divider()

    if st.button(
        "🌐 Change Language",
        use_container_width=True
    ):

        for key, value in defaults.items():
            st.session_state[key] = value

        st.rerun()

# =========================================
# FORCE BUTTON
# =========================================
if st.button(
    "🔄 Force New Riddle",
    use_container_width=True
):

    st.session_state.current_riddle = ""

    load_new_riddle()

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
# STATUS MESSAGE
# =========================================
if st.session_state.status_msg != "":

    if "Correct" in st.session_state.status_msg:

        st.success(st.session_state.status_msg)

    elif "Wrong" in st.session_state.status_msg:

        st.warning(st.session_state.status_msg)

    else:

        st.error(st.session_state.status_msg)

# =========================================
# MAIN GAME
# =========================================
if st.session_state.real_answer != "":

    st.subheader("🧠 Your Riddle")

    st.info(st.session_state.current_riddle)

    # =====================================
    # HINT BUTTON
    # =====================================
    if st.button("💡 Get Hint (-2 points)"):

        if st.session_state.streak >= 2:

            with st.spinner("Generating hint..."):

                st.session_state.hint = generate_hint(
                    st.session_state.current_riddle,
                    st.session_state.real_answer,
                    st.session_state.language
                )

                st.session_state.streak -= 2

                st.rerun()

        else:

            st.warning("Need at least 2 points!")

    # =====================================
    # SHOW HINT
    # =====================================
    if st.session_state.hint:

        st.warning(
            f"💡 Hint: {st.session_state.hint}"
        )

    # =====================================
    # ANSWER FORM
    # =====================================
    if not st.session_state.show_next:

        with st.form("answer_form"):

            user_guess = st.text_input(
                "Your Answer",
                placeholder="Type answer here..."
            )

            submitted = st.form_submit_button(
                "✅ Submit Answer",
                use_container_width=True
            )

            if submitted:

                correct_answer = (
                    st.session_state.real_answer
                    .strip()
                    .lower()
                )

                player_answer = (
                    user_guess
                    .strip()
                    .lower()
                )

                if player_answer == correct_answer:

                    st.session_state.status_msg = (
                        f"🎉 Correct! "
                        f"Answer was: "
                        f"{st.session_state.real_answer}"
                    )

                    st.session_state.streak += 10

                    if (
                        st.session_state.streak >
                        st.session_state.high_score
                    ):

                        st.session_state.high_score = (
                            st.session_state.streak
                        )

                    st.session_state.show_next = True

                else:

                    st.session_state.lives -= 1

                    if st.session_state.lives <= 0:

                        st.session_state.status_msg = (
                            f"💀 Game Over! "
                            f"Answer was: "
                            f"{st.session_state.real_answer}"
                        )

                        st.session_state.streak = 0

                        st.session_state.show_next = True

                    else:

                        st.session_state.status_msg = (
                            f"❌ Wrong! "
                            f"{st.session_state.lives} lives left."
                        )

                st.rerun()

    # =====================================
    # NEXT BUTTON
    # =====================================
    if st.session_state.show_next:

        st.markdown("---")

        if st.button(
            "➡️ NEXT RIDDLE",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.current_riddle = ""
            st.session_state.real_answer = ""
            st.session_state.hint = ""
            st.session_state.show_next = False
            st.session_state.status_msg = ""

            load_new_riddle()

            st.rerun()