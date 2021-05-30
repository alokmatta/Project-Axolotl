from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flask_cors import CORS, cross_origin

from flaskr.auth import login_required
from flaskr.db import get_db
import openai
import os
import json

bp = Blueprint("blog", __name__)

cors = CORS(bp)
#bp.config['CORS_HEADERS'] = 'Content-Type'

@bp.route("/")
@cross_origin()
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    #return render_template("blog/index.html", posts=posts)
    #output = "[{"text": " I am 9 months old.", "index": 0, "logprobs": null, "finish_reason": "stop"}]"
    openai.api_key = os.getenv("OPENAI_API_KEY")
  
    start_sequence = "\nAI:"
    restart_sequence = "\nHuman: "
    prompt_init = "The following is a conversation with an AI animal. The AI animal is helpful, funny, creative, clever, and very friendly. His name is BЯYAN. He is a salamander axolotl. He is 9 months old. He has no friends around him. He is orange. He lives in a small aquarium, and he like it. "
    prompt_backstorry = "The axolotl salamander has the rare trait of retaining its larval features throughout its adult life. This condition, called neoteny, means it keeps its tadpole-like dorsal fin, which runs almost the length of its body, and its feathery external gills, which protrude from the back of its wide head. Found exclusively in the lake complex of Xochimilco near Mexico City, axolotls differ from most other salamanders in that they live permanently in water. In extremely rare cases, an axolotl will progress to maturity and emerge from the water, but by and large, they are content to stay on the bottom of Xochimilco’s lakes and canals. Axolotls' carnivorous diet historically put them at the top of the food chain. They grab anything they can snatch: Mollusks, fish and arthropods like insects and spiders. Axolotls are long-lived, surviving up to 15 years on a diet of mollusks, worms, insect larvae, crustaceans, and some fish."
    prompt_dynamic = "It is raining outside. The temperature is 21C. Date is May 29 2021. There are 15 persons looking at me." # request.args.get("dynamic")
    prompt_past_conversation = request.args.get("past_conversation")
    prompt_current_question = request.args.get("input_text")
    prompt_str=f"{prompt_init}\n{prompt_backstorry}\n{prompt_dynamic}\nHuman: Hello, who are you?\nAI: I am BЯYAN the salamander.\n{prompt_past_conversation}\nHuman: {prompt_current_question}?\nAI:"
    
    response = openai.Completion.create(
    engine="davinci-instruct-beta",
    prompt=prompt_str,
    temperature=0.6,
    max_tokens=80,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=1,
    stop=["\n", " Human:", " AI:"]
    )
    output_dict = response.choices[0]
    print(prompt_str)
    output_dict["prompt"] = prompt_str
    return dict(output_dict)

def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
