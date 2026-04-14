# 🎵 Music Recommender Simulation

## Project Summary

Real-world systems utilize a two-stage pipeline—candidate retrieval and fine-grained ranking—to filter massive libraries into personalized lists. My simulation will focus on the ranking stage through content-based filtering, prioritizing the specific "DNA" of a track to ensure accuracy without needing massive interaction logs. The 'Song' object contain an ID, title, genre, and numerical energy, danceability, and valence values. The 'UserProfile' objects will store a username, favorite genres, target attribute values, and importance weights. This algorithm ranks songs based on how closely their features align with a user’s ideal musical profile.

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

In my system, each song has eight features including genre, mood, energy, valence, danceability, bpm, acousticness and loudness. Genre and mood are both categorical labels, while energy, which tracks how intense or active thr track feels, and valence, which measures emotional positivity,  are both floats. Danceability is also a float, tracking how the rhythm will most likely make the user dance. Bpm is an integer that tracks the amount of beats per minute (tempo). Acousticness (a float) compares how acoustic or produced a track may sound, while loudness (also a float) tracks the overall volume level. 

The UserProfile has 6 features: preferred_genre, preferred mood, target_energy, target_valence, target_danceability (floats), target_bpm (int), target_acousticness, target_loudness and top_k (how many reccomendations to return). 

The Reccomender computes a score for each song by first comparing the song's categorical fields to the user's preferences using these match rules:

genre_score = 25  if song.genre == user.preferred_genre
            = 18  if is_related_genre(song.genre, user.preferred_genre)
            = 0   otherwise

mood_score  = 20  if song.mood == user.preferred_mood
            = 14  if is_adjacent_mood(song.mood, user.preferred_mood)
            = 0   otherwise

Then, for each numeric feature, the reccomender scores each numeric feature, the energy and valence weighted highest at 15 pts each, danceability and BPM at 10 pts each, and acousticness and loudness at 3 and 2 pts respectively. After every song in the CSV is scored, the full list is sorted descending, a tie-break rule de-duplicates genre when two songs fall within 2 points of each other, and the top K results are returned. 

Reccomendations are made through first, score all in the songs in the CSV aaginst the User Profile. Next, sorting out the list by thr highest score. The, if two songs land within ~2 points of each other, the system prefers the one that adds a different genre to the list. This prevents reccomended songs from all being the same genre just because genre is worth 25 points. Finally, the system slices the first K entries and return them. K is a parameter the user (or the calling code) sets. 

The formula for the score is feature_score = weight × (1 − |user_target − song_value| / scale). Potential biases that may dsirupt this system are genre dominance, BPM scale sensitivity, and the blindless of populairty.
---

### CLI Verification

![alt text](<Screenshot 2026-04-14 at 2.55.18 PM.png>)

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

