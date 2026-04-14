from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv

RELATED_GENRES = {
    "pop": {"indie pop", "synthwave", "reggaeton", "afrobeats"},
    "indie pop": {"pop", "lofi", "synthwave"},
    "lofi": {"ambient", "jazz", "indie pop", "blues"},
    "ambient": {"lofi", "classical", "jazz"},
    "jazz": {"blues", "lofi", "ambient"},
    "blues": {"jazz", "country", "lofi"},
    "rock": {"metal", "hip-hop", "pop"},
    "metal": {"rock", "hip-hop"},
    "hip-hop": {"reggaeton", "afrobeats", "rock", "metal"},
    "reggaeton": {"hip-hop", "pop", "afrobeats"},
    "afrobeats": {"reggaeton", "pop", "hip-hop"},
    "synthwave": {"pop", "indie pop", "rock"},
    "country": {"blues", "rock", "classical"},
    "classical": {"ambient", "country"},
}

ADJACENT_MOODS = {
    "happy": {"playful", "confident", "party", "nostalgic"},
    "chill": {"relaxed", "focused", "serene", "moody"},
    "intense": {"aggressive", "confident", "party"},
    "relaxed": {"chill", "serene", "nostalgic"},
    "focused": {"chill", "moody", "confident"},
    "moody": {"melancholic", "focused", "chill", "nostalgic"},
    "melancholic": {"moody", "nostalgic", "serene"},
    "confident": {"happy", "intense", "party", "focused"},
    "aggressive": {"intense", "confident"},
    "nostalgic": {"melancholic", "relaxed", "happy", "moody"},
    "party": {"happy", "playful", "confident", "intense"},
    "serene": {"chill", "relaxed", "melancholic"},
    "playful": {"happy", "party", "confident"},
}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    loudness: float

    def to_dict(self) -> Dict:
        """Return this song as a dictionary used by scoring helpers."""
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "genre": self.genre,
            "mood": self.mood,
            "energy": self.energy,
            "tempo_bpm": self.tempo_bpm,
            "bpm": self.tempo_bpm,
            "valence": self.valence,
            "danceability": self.danceability,
            "acousticness": self.acousticness,
            "loudness": self.loudness,
        }

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    preferred_genre: str
    preferred_mood: str
    target_energy: float
    target_valence: float
    target_danceability: float
    target_bpm: int
    target_acousticness: float
    target_loudness: float
    top_k: int = 5

    def to_prefs_dict(self) -> Dict:
        """Return user targets in the dictionary shape expected by score_song."""
        return {
            "genre": self.preferred_genre,
            "mood": self.preferred_mood,
            "energy": self.target_energy,
            "valence": self.target_valence,
            "danceability": self.target_danceability,
            "bpm": self.target_bpm,
            "acousticness": self.target_acousticness,
            "loudness": self.target_loudness,
        }

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the song catalog used for recommendations."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = None) -> List[Song]:
        """Rank songs for a user and return the top-k recommendations."""
        k = k or user.top_k
        prefs = user.to_prefs_dict()

        scored: List[Tuple[float, Song]] = []
        for song in self.songs:
            score, _ = score_song(prefs, song.to_dict())
            scored.append((score, song))

        scored.sort(key=lambda item: item[0], reverse=True)

        results: List[Song] = []
        seen_genres: set = set()
        last_kept_score = None

        for score, song in scored:
            if last_kept_score is None:
                results.append(song)
                seen_genres.add(song.genre.lower())
                last_kept_score = score
                if len(results) >= k:
                    break
                continue

            within_tiebreak = abs(score - last_kept_score) <= 2.0
            if within_tiebreak and song.genre.lower() in seen_genres:
                continue

            results.append(song)
            seen_genres.add(song.genre.lower())
            last_kept_score = score

            if len(results) >= k:
                break

        if len(results) < k:
            for _, song in scored:
                if song not in results:
                    results.append(song)
                if len(results) >= k:
                    break

        return results[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate a readable score-and-reasons summary for one song."""
        prefs = user.to_prefs_dict()
        total_score, reasons = score_song(prefs, song.to_dict())

        lines = [
            f"'{song.title}' by {song.artist}  -  score: {total_score:.1f}/100",
            "-" * 48,
        ]
        for reason in reasons:
            lines.append(f"  {reason}")

        return "\n".join(lines)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dictionaries."""
    songs: List[Dict] = []

    with open(csv_path, mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            loudness_value = row.get("loudness", "")
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": int(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "loudness": float(loudness_value) if loudness_value not in ("", None) else 0.0,
            }
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Compute a weighted score and human-readable reasons for one song."""
    score = 0.0
    reasons: List[str] = []

    user_genre = str(user_prefs.get("genre", "")).strip().lower()
    song_genre = str(song.get("genre", "")).strip().lower()
    if user_genre and song_genre:
        if user_genre == song_genre:
            score += 12.5
            reasons.append("genre match (+12.5)")
        elif (
            song_genre in RELATED_GENRES.get(user_genre, set())
            or user_genre in RELATED_GENRES.get(song_genre, set())
        ):
            score += 9.0
            reasons.append("related genre (+9.0)")

    user_mood = str(user_prefs.get("mood", "")).strip().lower()
    song_mood = str(song.get("mood", "")).strip().lower()
    if user_mood and song_mood:
        if user_mood == song_mood:
            score += 20.0
            reasons.append("mood match (+20.0)")
        elif (
            song_mood in ADJACENT_MOODS.get(user_mood, set())
            or user_mood in ADJACENT_MOODS.get(song_mood, set())
        ):
            score += 14.0
            reasons.append("adjacent mood (+14.0)")

    numeric_specs = {
        "energy": (30.0, 1.0),
        "valence": (15.0, 1.0),
        "danceability": (10.0, 1.0),
        "bpm": (10.0, 150.0),
        "acousticness": (3.0, 1.0),
        "loudness": (2.0, 60.0),
    }

    for feature, (weight, scale) in numeric_specs.items():
        user_value = float(user_prefs.get(feature, 0.0))
        if feature == "bpm":
            song_value = float(song.get("bpm", song.get("tempo_bpm", 0.0)))
        else:
            song_value = float(song.get(feature, 0.0))

        feature_score = weight * (1.0 - abs(user_value - song_value) / scale)
        contribution = max(0.0, feature_score)
        score += contribution
        if contribution > 0:
            reasons.append(f"{feature} match (+{contribution:.1f})")

    return float(min(100.0, score)), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score and sort songs, returning the top-k results with reasons."""
    scored_songs = [
        (song, score, reasons if reasons else ["No strong matches"])
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]
