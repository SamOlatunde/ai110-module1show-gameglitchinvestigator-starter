# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- **Attempt counter starts one too low across all difficulty levels.** The game appears to count an attempt before the player makes a guess. For example, in Normal mode (8 attempts allowed), the game immediately shows only 7 attempts remaining at the start of a new game.

- **Higher/lower hint logic is reversed.** When the player's guess is higher than the secret number, the game incorrectly instructs the player to guess higher instead of lower, and vice versa. For example, in Normal mode, entering `50` resulted in a "go higher" hint even though the correct answer was `9`.

- **"Submit Guess" stops working after starting a new game.** Once a game ends and **New Game** is clicked, the **Submit Guess** button becomes unresponsive.

- **Show Hint toggle does not restore existing hints.** Unchecking **Show Hint** correctly hides the hint, but rechecking it does not display the current hint again. The hint only reappears after submitting another guess while the option is enabled.

- **Attempts value is incorrectly initialized in debug information.** Each time the page is loaded, the attempts field in the developer debug panel is set to `1` for all difficulty levels instead of starting at `0`.

- **Instructions do not update based on difficulty.** The game always displays "Guess a number between 1 and 100" regardless of the selected difficulty, even though each difficulty level has a different valid range.

- **Difficulty changes do not reset game state correctly.** Switching between difficulty levels does not generate a new secret number or update values to match the selected mode. For example, starting in Normal mode with a secret number of `96` and then switching to Hard or Easy mode leaves the secret number unchanged, even when it falls outside the valid range for those difficulties. The game still allows play with this invalid setup.

- **Guess history in debug information does not reset or update correctly.** Clicking **New Game** does not clear the history list, and the list updates with a delay. Instead of showing the latest guess immediately, it displays guesses from one or two turns earlier.

- **Score calculation may be incorrect.** Guessing the correct answer on the first attempt resulted in a score of `77`. If first-attempt success is intended to receive the maximum possible score (or a higher score than 77), the scoring formula may not be calculating points correctly. Theres also negative scores


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

## Bug Reproduction Logs

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Start a new game in **Normal** mode (8 attempts allowed) | Attempts remaining should display **8** before any guesses are made | Attempts remaining displays **7**, indicating an attempt has already been counted | No console error observed |
| In **Normal** mode, with secret number set to `9` (visible in debug info), enter a guess of `50` and submit | Game should display a hint instructing the player to guess **lower** | Game incorrectly displays a hint instructing the player to guess **higher** | No console error observed |
| Complete a game, click **New Game**, then enter a guess and click **Submit Guess** | A new game should start and the guess should be processed normally | **Submit Guess** button becomes unresponsive and no guess is processed | No console error observed |
 

---

## 2. How did you use AI as a teammate?

### Correct
- On my first run after fixing the bugs, I noticed that the balloons and winning message where no longer showing. I highlighted relevant code and prompted clause to explain why that was happening. It explained that this was due to a rerun I added at the end of the submit branch to make sure there was no delay in loading history in developer debug info. Claude sugessted to only rerender the page when the user was still playing (status==playing) and made the change. To verify, I launched the website and entered a correct guess. I observed that the balloons and winning message showed.

### Incorrect
- I instructed claude to fix the issue that was letting me switch modes without restarting the game and resetting state variable. It reset state variables in the new game branch and mandated a rerun but while doing that, it initialized the seceret using (1,100) which is only correct using normal mode. I found this out while switchign through modes mide game to see if the variables were properly reset. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I repeated actions and input that originally produced incorrect results or caused the game to break. If the correct output was produced or the game didn't break, then the bug was really fixed.
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  - I played the game in all difficulty levels multiple times,running out of attempts on purpose, and trying to win like a real user to see i hte game works as expected.
- Did AI help you design or understand any tests? How?
  - I instructed claude to design exhaustive pytest cases for the check_guess and parse_guess functions.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
