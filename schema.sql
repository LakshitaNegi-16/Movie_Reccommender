
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genres TEXT NOT NULL,
    description TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS watchlist (
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    watched INTEGER DEFAULT 0,

    PRIMARY KEY (user_id, movie_id),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (movie_id)
        REFERENCES movies(movie_id)
);

CREATE TABLE IF NOT EXISTS ratings (
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL NOT NULL
        CHECK (rating >= 0.5 AND rating <= 5.0),

    PRIMARY KEY (user_id, movie_id),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (movie_id)
        REFERENCES movies(movie_id)
);
