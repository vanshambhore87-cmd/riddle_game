import streamlit as st
import random
import time

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(page_title="Riddle Master", page_icon="🧩", layout="centered")

# =========================================
# THE OFFLINE DATABASE (Add your 100+ here!)
# =========================================
RIDDLES_DB = {
    "English": [
        {"riddle": "What has hands but cannot clap?", "answer": "clock", "hint": "It hangs on a wall and ticks."},
        {"riddle": "What has keys but no locks?", "answer": "piano", "hint": "It makes beautiful music."},
        {"riddle": "I have branches, but no fruit, trunk or leaves. What am I?", "answer": "bank", "hint": "A place that holds money."},
        {"riddle": "What has one eye, but can't see?", "answer": "needle", "hint": "Used for sewing clothes."},
        {"riddle": "What has legs, but doesn't walk?", "answer": "table", "hint": "You eat your dinner on it."}
    ],
    "Hindi": [
        {"riddle": "काला घोड़ा, सफेद सवारी, एक उतरा तो दूसरे की बारी।", "answer": "तवा", "hint": "रोटी बनाने के काम आता है।"},
        {"riddle": "एक फूल काले रंग का, सिर पर हमेशा सुहाए।", "answer": "छतरी", "hint": "बारिश में काम आती है।"},
        {"riddle": "कटोरी पे कटोरी, बेटा बाप से भी गोरा।", "answer": "प्याज", "hint": "काटते समय आंसू आते हैं।"},
        {"riddle": "लाल पूंछ हरी बिलाई, इसका हल बता मेरे भाई।", "answer": "मूली", "hint": "यह एक सफेद सब्जी/सलाद है।"},
        {"riddle": "बीमार नहीं रहती, फिर भी खाती है गोली।", "answer": "बंदूक", "hint": "सैनिक इसका इस्तेमाल करते हैं।"}
    ],
    "Marathi": [
        {"riddle": "दोन भाऊ शेजारी, भेट नाही संसारी.", "answer": "डोळे", "hint": "आपण यातून पाहतो."},
        {"riddle": "हिरवा रावा, लाल रस्ता, आत मध्ये काळ्या बिया.", "answer": "कलिंगड", "hint": "उन्हाळ्यात खातात ते फळ."},
        {"riddle": "बत्तीस चिंचोके, त्यात एकच साप.", "answer": "जीभ", "hint": "तोंडात असते आणि चव समजते."},
        {"riddle": "काळा कुत्रा, भिंतीला घासला की लाल होतो.", "answer": "काडीपेटी", "hint": "आग लावण्यासाठी वापरतात."},
        {"riddle": "एका म्हातारीला बारा मुले, तरीही ती एकटीच.", "answer": "घड्याळ", "hint": "वेळ दाखवते."}
    ]
}

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
    "show_next": False,
    "status_msg": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================
# GAME ENGINE FUNCTIONS
# =========================================
def load_new_riddle():
    # Pick a random riddle from the chosen language list!
    chosen_riddle = random.choice(RIDDLES_DB[st.session_state.language])
    
    st.session_state.current_riddle = chosen_riddle["riddle"]
    st.session_state.real_answer = chosen_riddle["answer"]
    # We load the hint instantly but hide it until they click the button
    st.session_state.hidden_hint = chosen_riddle["hint"] 
    
    st.session_state.hint = ""
    st.session_state.lives = 3
    st.session_state.show_next = False
    st.session_state.status_msg = ""

# =========================================
# LANGUAGE SELECTOR UI
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
# MAIN APP UI
# =========================================
st.title(f"🧩 Riddle Master ({st.session_state.language})")

with st.sidebar:
    st.header("⚙️ Settings")
    st.success("⚡ Offline Mode Active (Zero Lag)")
    st.divider()
    if st.button("🌐 Change Language", use_container_width=True):
        for key, value in defaults.items():
            st.session_state[key] = value
        st.rerun()

# SCOREBOARD
a, b, c = st.columns(3)
a.metric("🔥 Streak", st.session_state.streak)
b.metric("🏆 High Score", st.session_state.high_score)
c.metric("❤️ Lives", st.session_state.lives)
st.divider()

# =========================================
# GAMEPLAY LOOP
# =========================================
if st.session_state.current_riddle == "":
    load_new_riddle()
    st.rerun() # Instant reload without loading spinner!

if st.session_state.current_riddle:
    st.subheader("🧠 Your Riddle")
    st.info(st.session_state.current_riddle)

    # Hint Button
    if st.button("💡 Get Hint (-2 points)"):
        if st.session_state.streak >= 2:
            st.session_state.hint = st.session_state.hidden_hint
            st.session_state.streak -= 2
            st.rerun()
        else:
            st.warning("Need at least 2 points!")
            
    if st.session_state.hint:
        st.warning(f"💡 Hint: {st.session_state.hint}")

    # Status Messages
    if st.session_state.status_msg:
        if "Correct" in st.session_state.status_msg:
            st.success(st.session_state.status_msg)
        elif "Wrong" in st.session_state.status_msg:
            st.warning(st.session_state.status_msg)
        else:
            st.error(st.session_state.status_msg)

    # Input Form 
    if not st.session_state.show_next:
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

    # Next Button
    if st.session_state.show_next:
        st.markdown("---")
        if st.button("➡️ GET NEXT RIDDLE", use_container_width=True, type="primary"):
            st.session_state.current_riddle = ""
            st.session_state.status_msg = ""
            st.session_state.show_next = False 
            st.rerun()
