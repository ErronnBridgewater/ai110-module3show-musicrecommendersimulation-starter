# Reflection — Music Recommender Evaluation

## Profile Comparisons

### High-Energy Pop vs. Chill Lofi

These two profiles produced opposite results as expected. Pop focuses on loud, fast tracks for movement, while Lofi picks slow, quiet songs for focusing. Since their settings for energy and tempo were so far apart, the two lists had zero songs in common. This shows that the scoring formula effectively separates different styles.
---

### High-Energy Pop vs. Deep Intense Rock

While both styles are loud and fast, they diverged from each other because of mood and genre. Pop looks for "happy" music while Rock seeks "intense" tracks, and the system treats these as unrelated. The Rock profile’s quality dropped quickly because the small dataset lacked enough actual rock songs. In turn, the system was eventually forced recommend pop tracks that matched the "energy" numbers.

---

### Chill Lofi vs. Deep Intense Rock

This pair showed the biggest gap in success based on what music was available. The Lofi profile had several high-scoring matches because the dataset was full of chill and ambient songs. In contrast, the Rock profile struggled and produced much lower scores because it only had one perfect match to choose from, proving that the algorithm is only as good as the variety of songs in its library.

---