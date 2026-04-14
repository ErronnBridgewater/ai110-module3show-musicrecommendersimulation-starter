"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


# Profile 1 — High-Energy Pop
user_prefs_pop = {
    "genre":        "pop",
    "mood":         "happy",
    "energy":       0.88,
    "valence":      0.82,
    "danceability": 0.85,
    "bpm":          125,
    "acousticness": 0.10,
    "loudness":     -4.0,
}

# Profile 2 — Chill Lofi
user_prefs_lofi = {
    "genre":        "lofi",
    "mood":         "chill",
    "energy":       0.38,
    "valence":      0.58,
    "danceability": 0.60,
    "bpm":          76,
    "acousticness": 0.80,
    "loudness":     -14.0,
}

# Profile 3 — Deep Intense Rock
user_prefs_rock = {
    "genre":        "rock",
    "mood":         "intense",
    "energy":       0.92,
    "valence":      0.35,
    "danceability": 0.55,
    "bpm":          148,
    "acousticness": 0.08,
    "loudness":     -3.5,
}



def main() -> None:
    songs = load_songs("data/songs.csv")
    profiles = [
        ("High-Energy Pop",   user_prefs_pop),
        ("Chill Lofi",        user_prefs_lofi),
        ("Deep Intense Rock", user_prefs_rock),
    ]

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for label, user_prefs in profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print(f"\n{'=' * 72}")
        print(f"Profile: {label}")
        print("=" * 72)
        for rank, rec in enumerate(recommendations, start=1):
            song, score, reasons = rec
            print(f"{rank}. {song['title']}")
            print(f"   Final Score : {score:.2f}")
            print("   Reasons:")
            for reason in reasons:
                print(f"   - {reason}")
            print("-" * 72)

if __name__ == "__main__":
    main()
