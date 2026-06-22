import random
import streamlit as st
# REFACTOR: parse_guess and check_guess moved to logic_utils.py so they can be
# imported and unit-tested independently of Streamlit
from logic_utils import INITIAL_ATTEMPTS, parse_guess, check_guess

# check_guess now returns a plain outcome string ("Win", "Too High", "Too Low").
# HINT_MESSAGES maps those outcomes to display text, keeping UI copy out of the logic layer.
HINT_MESSAGES = {
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
    "Win": "🎉 Correct!",
}

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100



def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        # FIX: removed `+ 1` offset so attempt 0 earns full 100 points instead of 90
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIX: replaced arbitrary ±5 parity logic with a flat -5 penalty floored at 0 to prevent negative scores
    if outcome == "Too High":
        return max(0, current_score - 5)
    if outcome == "Too Low":
        return max(0, current_score - 5)

    return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

# FIX: track active difficulty in session state; when it changes, reset all game state and regenerate secret within the new range
if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.last_outcome = None
    st.session_state.difficulty_changed_msg = f"Switched to {difficulty} mode. New game started!"
    st.rerun()

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = INITIAL_ATTEMPTS  #FIX: was hardcoded to 1, so `attempt_limit - attempts` showed 7 instead of 8 on load; moved to logic_utils as INITIAL_ATTEMPTS = 0 so a unit test can catch a regression

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "last_outcome" not in st.session_state:
    st.session_state.last_outcome = None

if st.session_state.get("difficulty_changed_msg"):
    st.success(st.session_state.difficulty_changed_msg)
    st.session_state.difficulty_changed_msg = None

st.subheader("Make a guess")


st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:  #FIX: reset status, history, and score — previously only attempts/secret were reset, leaving status as "won"/"lost" which caused st.stop() to block the submit handler on the next game
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high) #FIX: switch from hard coded (1,100), to (low,high) to fix
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.last_outcome = None
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: original converted secret to str on even attempts, causing lexicographic comparison and wrong hints
        secret = st.session_state.secret

        outcome = check_guess(guess_int, secret)

        st.session_state.last_outcome = outcome

        # FIX: pass attempts - 1 so a first-guess win uses attempt_number=0, matching the scoring formula's intent
        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts - 1,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

    # FIX: rerun after submit so debug panel (rendered before this block) re-renders with updated history/attempts; skip rerun on win/loss so balloons and end messages are not wiped
    if st.session_state.status == "playing":
        st.rerun()

# FIX: moved hint display outside the submit block and read from session state so toggling the checkbox re-shows the last hint without requiring a new guess
if show_hint and st.session_state.last_outcome:
    st.warning(HINT_MESSAGES[st.session_state.last_outcome])

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
