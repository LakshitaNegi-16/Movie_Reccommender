
# CineMatch - Recommendation Engine
# Part 3: Python + SQL

from database import get_movies


def recommend_movies(preferred_genres, watched_ids=None, limit=5):
    """
    Recommend movies based on genre preferences.

    preferred_genres: list of genres the user likes
    watched_ids: movie IDs the user has already watched
    limit: maximum number of recommendations
    """

    if watched_ids is None:
        watched_ids = set()
    else:
        watched_ids = set(watched_ids)

    # Normalize genres so capitalization does not matter.
    preferred_genres = {
        genre.strip().lower()
        for genre in preferred_genres
        if genre.strip()
    }

    movies = get_movies()
    recommendations = []

    for movie_id, title, genres, description in movies:

        # Skip movies already watched.
        if movie_id in watched_ids:
            continue

        # Convert "Sci-Fi|Drama" into a list of genres.
        movie_genres = {
            genre.strip().lower()
            for genre in genres.split("|")
        }

        # Count how many genres match.
        score = len(preferred_genres & movie_genres)

        # Only recommend movies with matching genres.
        if score > 0:
            recommendations.append({
                "movie_id": movie_id,
                "title": title,
                "genres": genres,
                "description": description,
                "score": score
            })

    # Highest matching score comes first.
    recommendations.sort(
        key=lambda movie: (
            -movie["score"],
            movie["title"].lower()
        )
    )

    return recommendations[:max(0, limit)]


def search_movies(query):
    """Search for movies by title."""

    query = query.strip().lower()

    if not query:
        return []

    movies = get_movies()

    return [
        {
            "movie_id": movie_id,
            "title": title,
            "genres": genres,
            "description": description
        }
        for movie_id, title, genres, description in movies
        if query in title.lower()
    ]


# Run a simple test when this file is executed directly.
if __name__ == "__main__":

    print("CINEMATCH RECOMMENDATION ENGINE")
    print("-" * 35)

    genre_input = input(
        "Enter genres you like, separated by commas: "
    )

    preferred_genres = genre_input.split(",")

    watched_input = input(
        "Enter watched movie IDs separated by commas, "
        "or press Enter to skip: "
    )

    watched_ids = set()

    for value in watched_input.split(","):
        value = value.strip()

        if value.isdigit():
            watched_ids.add(int(value))

    results = recommend_movies(
        preferred_genres,
        watched_ids=watched_ids,
        limit=5
    )

    if results:
        print("\nYour recommendations:\n")

        for number, movie in enumerate(results, start=1):
            print(f"{number}. {movie['title']}")
            print(f"   Genres: {movie['genres']}")
            print(f"   Match score: {movie['score']}")
            print(f"   {movie['description']}\n")
    else:
        print("No matching movies found. Try other genres.")
