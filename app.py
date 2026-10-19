
from flask import Flask, render_template, request
from database import initialize_database, get_movies
from recommender import recommend_movies

app = Flask(__name__)

# Prepare the database
initialize_database()


@app.route("/", methods=["GET", "POST"])
def home():
    movies = get_movies()
    recommendations = []
    genres_input = ""

    if request.method == "POST":
        genres_input = request.form.get("genres", "")
        watched_input = request.form.get("watched_ids", "")

        preferred_genres = genres_input.split(",")

        watched_ids = set()
        for value in watched_input.split(","):
            value = value.strip()
            if value.isdigit():
                watched_ids.add(int(value))

        recommendations = recommend_movies(
            preferred_genres,
            watched_ids=watched_ids,
            limit=5
        )

    return render_template(
        "index.html",
        movies=movies,
        recommendations=recommendations,
        genres_input=genres_input
    )


if __name__ == "__main__":
    app.run(debug=True)
