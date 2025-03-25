import pandas as pd
import json


def load_and_filter_movies():
    title_basics = pd.read_csv(
        "title.basics.tsv", sep="\t", low_memory=False, na_values="\\N"
    )

    movies = title_basics[title_basics["titleType"] == "movie"].dropna(
        subset=["tconst", "originalTitle", "startYear", "runtimeMinutes", "genres"]
    )
    movies = movies.head(500)

    movies.to_csv("filtered_movies.csv", index=False)
    print("Filtered movies saved.")


def process_akas():
    title_akas = pd.read_csv(
        "title.akas.tsv", sep="\t", low_memory=False, na_values="\\N"
    )
    movies = pd.read_csv("filtered_movies.csv")
    print("Loaded AKA data.")

    relevant_akas = title_akas[title_akas["titleId"].isin(movies["tconst"])]

    original_languages = (
        relevant_akas.groupby("titleId")["language"].first().dropna().to_dict()
    )
    original_countries = (
        relevant_akas.groupby("titleId")["region"].first().dropna().to_dict()
    )

    with open("languages.json", "w", encoding="utf-8") as f:
        json.dump(original_languages, f, indent=4, ensure_ascii=False)

    with open("countries.json", "w", encoding="utf-8") as f:
        json.dump(original_countries, f, indent=4, ensure_ascii=False)

    print("Languages and countries saved.")


def process_people():
    title_principals = pd.read_csv(
        "title.principals.tsv", sep="\t", low_memory=False, na_values="\\N"
    )
    movies = pd.read_csv("filtered_movies.csv")

    relevant_principals = title_principals[
        title_principals["tconst"].isin(movies["tconst"])
    ]

    people_dict = (
        relevant_principals.groupby("tconst")[["nconst", "category", "job"]]
        .apply(lambda x: x.dropna().to_dict(orient="records"))
        .to_dict()
    )

    people_data = {
        tconst: {"peopleInvolved": people_dict.get(tconst, [])}
        for tconst in movies["tconst"]
    }

    with open("people.json", "w", encoding="utf-8") as f:
        json.dump(people_data, f, indent=4, ensure_ascii=False)

    print("People data saved.")


def combine_data():
    movies = pd.read_csv("filtered_movies.csv")

    with open("languages.json", "r", encoding="utf-8") as f:
        languages_dict = json.load(f)

    with open("countries.json", "r", encoding="utf-8") as f:
        countries_dict = json.load(f)

    with open("people.json", "r", encoding="utf-8") as f:
        people_dict = json.load(f)

    name_basics = pd.read_csv(
        "name.basics.tsv", sep="\t", low_memory=False, na_values="\\N"
    )
    name_dict = name_basics.set_index("nconst")["primaryName"].to_dict()

    genres_set = set()
    all_languages = set()
    all_countries = set()
    all_people = {}

    movies_list = []

    for _, movie in movies.iterrows():
        tconst = movie["tconst"]
        genres = movie["genres"].split(",")
        genres_set.update(genres)

        language = languages_dict.get(tconst)
        country = countries_dict.get(tconst, None)

        if language:
            all_languages.add(language)
        all_countries.add(country)

        movie_people = people_dict.get(tconst, {}).get("peopleInvolved", [])
        for person in movie_people:
            person_id = person["nconst"]
            person["name"] = name_dict.get(person_id, None)
            all_people[person_id] = person["name"]

        movie_data = {
            "id": tconst,
            "originalTitle": movie["originalTitle"],
            "duration": movie["runtimeMinutes"],
            "releaseYear": movie["startYear"],
            "genres": genres,
            "originalLanguage": language if language else None,
            "originalCountry": country,
            "peopleInvolved": movie_people,
        }

        movies_list.append(movie_data)

    data_output = {
        "movies": movies_list,
        "allGenres": list(genres_set),
        "allLanguages": list(all_languages),
        "allCountries": list(all_countries),
        "allPeople": all_people,
    }

    with open("imdb_movies.json", "w", encoding="utf-8") as f:
        json.dump(data_output, f, indent=4, ensure_ascii=False)

    print("Final JSON dataset created: imdb_movies.json")


load_and_filter_movies()
process_akas()
process_people()
combine_data()
