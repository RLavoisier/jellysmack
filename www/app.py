import requests
from flask import Flask, render_template, request
from requests import HTTPError

from settings import API_ROUTE, DEFAULT_PAGE_SIZE

app = Flask(__name__)


def get_pagination_context(response_json: dict) -> dict:
    """This method return the values for handling pagination on website"""
    total = response_json.get("total")
    page = response_json.get("page")
    size = response_json.get("size")
    previous = None
    next = None

    if page > 1:
        previous = page - 1

    if (page * size) <= (total - size):
        next = page + 1

    last = round(total / size)

    return {"page": page, "previous": previous, "next": next, "last": last}


@app.route("/")
def episode_list():
    params = {
        "page": request.args.get("page", 1),
        "size": request.args.get("pagesize", DEFAULT_PAGE_SIZE),
    }
    response = requests.get(API_ROUTE.format(endpoint="episodes"), params=params)
    response_json = response.json()
    episodes = response_json.get("items")
    context = {
        "title": "Episode list",
        "episodes": episodes,
        "pagination": get_pagination_context(response_json),
    }
    return render_template("index.html", **context)


@app.route("/episodes/<episode_id>")
def episode(episode_id: int):
    response = requests.get(API_ROUTE.format(endpoint=f"episodes/{episode_id}"))
    try:
        response.raise_for_status()
    except HTTPError:
        return render_template(
            "404.html",
            **{
                "title": "Oops Error 404",
                "message": "This episode might exists on interdimentional cable though...",
            },
        )
    episode = response.json()
    context = {"title": f"{episode['episode']} - {episode['name']}", "episode": episode}
    return render_template("episode.html", **context)


@app.route("/characters")
def character_list():
    params = {
        "page": request.args.get("page", 1),
        "size": request.args.get("pagesize", DEFAULT_PAGE_SIZE),
    }
    response = requests.get(API_ROUTE.format(endpoint="characters"), params=params)
    response_json = response.json()
    characters = response_json.get("items")
    context = {
        "title": "Character list",
        "characters": characters,
        "pagination": get_pagination_context(response_json),
    }
    return render_template("character_list.html", **context)


@app.route("/characters/<character_id>")
def character(character_id: int):
    response = requests.get(API_ROUTE.format(endpoint=f"characters/{character_id}"))
    try:
        response.raise_for_status()
    except HTTPError:
        return render_template(
            "404.html",
            **{
                "title": "Oops Error 404",
                "message": "This character is not in this dimension...",
            },
        )
    character = response.json()
    context = {"title": f"{character['name']}", "character": character}
    return render_template("character.html", **context)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8888)
