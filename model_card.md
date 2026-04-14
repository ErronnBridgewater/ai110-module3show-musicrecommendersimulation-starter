# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Model Name: ScoreBeats 

---

## 2. Intended Use  


Given the user's musical preferences, such as genre and mood, the reccomender will a small catalog and returns the five
songs that best match what the user described. The system assumes the user can accurately describe their own taste in
structured terms (e.g., "I want high energy, low acousticness, fast BPM"). It is designed for classroom exploration. It should be understood as a transparent simulation of how real recommenders make decisions, not as a replacement.


## 3. How the Model Works  


Let's say you're walking into a record store and hand the clerk a description of your perfect song. The clerk then
goes through every record in the store and gives each one a score based on how closely it matches your description. The record with the highest score would then go to the top of your pile.

That is the scoring appraoch of ScoreBeats. Every song in the catalog gets scored on eight categories. Two of them are categorical, genre and mood, and the rest are numeric. For genre, an exact match earns the full bonus; a related genre (like indie pop for a pop request) earns a partial bonus; anything else earns nothing. Mood works very similary with exact matches scoring higher than adjacent ones. For the numeric features, energy, valence, danceability, tempo, acousticness, and loudness, the system measures how far each song's value is from what the user asked for and converts that distance into points. A song that is very close earns nearly the full weight for that feature. On the other hand, a song that is far away earns close to zero.

All the points add up to a score between 0 and 100. The songs are then sorted from highest to lowest, and the top five are returned. A change I made from the starter logic was that if the scores of two songs are tied, the system prefers the one that introduces a different genre into the list. This prevents identical results. 


---

## 4. Data  


The catalog contains 17 songs loaded from a CSV file. Each row represents one song with a unique ID, title, artist, genre, mood, and six numeric audio features. The genres represented are pop, lofi, rock, ambient, jazz, synthwave, indie pop, blues, hip-hop, metal, country, reggaeton, classical, and afrobeats. The moods represented are happy, chill, intense, relaxed, focused, moody, melancholic, confident, aggressive, nostalgic, party, serene, and playful.

No songs were removed from the original dataset, as I only added 7 other songs for testing. The most notable gap was how much each genre covered the songs. Lofi has three songs, pop has two, and most other genres have exactly one. Several
genres and moods like metal, reggaeton, blues, and nostalgic, have only one representative or none at all. The catalog also skews toward Western popular genres and does not meaningfully represent global music traditions.


## 5. Strengths  


The system works best for users whose preferences align with well-represented genres. The Chill Lofi profile serves as the best demonstration of the system’s accuracy. By matching lofi tracks with similar ambient songs, it achieved high scores of 98.14 and 98.03. These scores would resonate well with an actual listener. Additionally, the system provides clear justifications for its rankings, allowing users to easily understand and trust the underlying logic rather than just receiving a standard list they have made themselves.

The genre and mood tables also captured some non-obvious relationships correctly. Spacewalk Thoughts (ambient) ranking ahead of Coffee Shop Stories (jazz) for the Chill Lofi profile surprised me at first, but the reasons output showed that an ambient song with an exactly matching mood outscored a jazz song with only an adjacent mood. This demonstrated that the system working as designed.

---

## 6. Limitations and Bias 

There is no listening history, skip behavior, or repeat behavior that is used. As a result, recommendations are based only on one static preference.
No contextual signals are used, such as the time of day, activity, device, and etc.
No novelty, diversity, popularity, or fairness terms are included in scoring; songs are ranked by total score only in the recommender.
Diversity of the artists is not enforced, so the same artist can appear repeatedly if scores are high.


The catalog has only 10 songs, with concentration in lofi and pop, while several genres in the relationship map never appear in data.
Present genres are mainly pop, lofi, rock, ambient, jazz, synthwave, indie pop in the song dataset.
Missing from catalog despite being in the logic: metal, hip-hop, reggaeton, afrobeats, blues, country, and classical.
Mood coverage is also sparse: happy, chill, intense, relaxed, moody, focused appear, while melancholic, confident, aggressive, nostalgic, party, serene, playful are absent in the song dataset compared with the recomender.

Energy can dominate outcomes because it has the largest numeric weight at 30.0 in the recomender, so high-energy users are repeatedly pushed toward high-energy tracks.
Mood match is heavily rewarded (+20), which can keep recommendations in a narrow cluster.
Genre still adds a fixed bonus (+12.5 exact, +9 related), which can repeatedly prioritize familiar genres in the recomender.
Diversity control is limited to near-ties only, so non-tie cases still allow repetitive top results.

Users whose tastes align with well-represented genres/moods in the small catalog receive better matches than users preferring missing categories.
Users who provide complete numeric preferences are advantaged. This means missing numeric fields default to 0.0 and can skew results in the recomender.
Users with niche or cross-genre tastes may be disadvantaged because handcrafted genre/mood adjacency rules encode a limited worldview in the recommender.
Users seeking discovery are disadvantaged because the system has no explicit exploration mechanism and sorts strictly by scores in the recommender.



## 7. Evaluation  



The User Profiles I tested were High-Energy Pop, Chill Lofi, Deep Intense Rock. 
I focused on three things in the recommendations: whether the top result was an intuitive match, whether the score breakdown in the reasons list explained the ranking credibly, and whether the bottom of the top-5 still made reasonable sense or started to drift into songs that felt out of place.

High-Energy Pop returned Sunrise City (97.36) as its top result. Rooftop Lights came second at 89.80 on a related genre (+18) plus mood match, which makes sense since indie pop is a subgenre to pop. Storm Runner and Night Drive Loopm both scored in the low 60s on related genre alone with no mood match. This confirmed that the numeric features (energy, valence, danceability) separated them more than the qualitative scores.
Chill Lofi produced the tightest top songsL Library Rain (98.14) and Midnight Coding (98.03). Both are lofi/chill exact matches with nearly identical numeric profiles. Focus Flow ranked third at 92.76 with an adjacent mood (+14 instead of +20), and Spacewalk Thoughts ranked fourth at 86.66 as a related genre (ambient↔lofi) with a mood exact match. This is interesting beacuse it shwos that a slightly wrong genre but perfect mood can still rank above a genre match with a wrong mood.
Deep Intense Rock had the biggest drop-off in points. Storm Runner scored 96.36 as a genre and mood exact match, Gym Hero came second at 81.98 as a related genre with mood match (pop/intense), and then the list fell to Night Drive Loop at 63.48, Sunrise City at 59.33, and Rooftop Lights at just 40.47. That 40-point gap between first and fifth place is the largest across all three profiles.


Two things stood out. First, Gym Hero (pop/intense) ranking second for the Deep Intense Rock profile was unexpected. It had earned a related genre score because pop and rock share a relationship in RELATED_GENRES, and its mood was an exact match for "intense." On paper, it works as intended. However, a real user asking for rock probably wouldn't consider a pop gym track a satisfying second recommendation. 

Second, the Chill Lofi profile's 4th result, Spacewalk Thoughts ranking above Coffee Shop Stories was initially counterintuitive. Jazz feels closer to lofi than ambient does culturally. However, Spacewalk Thoughts had a mood exact match (+20) while Coffee Shop Stories only got an adjacent mood (+14)/ This confirmed that hat a single adjacenct boundary in mood can move a song by a full ranking position.

The first test I ran was reconstructing the scores by adding each reason line for a song to ensure the formula was computing as intended. Then I looked for scores in adjacent moods for songs, to confirm if the ADJACENT_MOODS dictionary was being read correctly. 


---

## 8. Future Work  

One idea for improving the model would be experimented songs I added. The current 17-song dataset is it was too small and too unevenly distributed to reveal whether the formula was actually good or just decent enough for the songs that happened to be there. Adding more songs,  especially in underrepresented genres like metal, reggaeton, blues, and classical, would help create real competition within each genre. It would force the scoring formula to make more narrow distinctions rather than defaulting to the only available match. 

Beyond data, I would like to add a feature so that the top-K results are required to span at least three distinct genres regardless of score. I would also add a contextual layer, like "time of day", so the same user gets different results at 7am versus midnight.

A long-term idea would be incorporating minimal interaction signals, like which songs the user skipped, replayed, or rated. This would provide a mroe hybrid approach to the system. 

---

## 9. Personal Reflection  


The biggest learning moment in this project was realizing how much the weights matter before a single song is even scored. I had to continously ask myself if genre more was important than how a song makes you feel? There was signifcant amount of abstract thought I had to put into this projet. 

Copilot helped significantly during implementation. It was useful for generating the
initial `score_song` structure, populating the genre and mood adjacency tables, and catching the `tempo_bpm` vs. `bpm` key mismatch before it became a runtime error. The places I needed to double check were anywhere the Agent made assumptions about weights or relationships that had not been validated against the actual data. 

What surprised me most was how complex the reccomendation system had actually gotten. It was not too long into the project where I had to find weighted scoring formulas, tie-break logic, genre relationship maps, and a reasons output that had to stay synchronized with every scoring decision. It was also very interesting, seeing how they were all connecting to each other across the main and reccomender files. 

If I extended this project, I would first build a small web interface so a user could enter preferences interactively and see the reasons output in real time. It would be more immersive than having to look at just the lines within the terminal. I would most likely implement streamlit into the project. 
