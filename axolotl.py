from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flask_cors import CORS, cross_origin

import openai
import os
import json

bp = Blueprint("blog", __name__)

cors = CORS(bp)
#bp.config['CORS_HEADERS'] = 'Content-Type'

@bp.route("/")
@cross_origin()
def index():

    openai.api_key = os.getenv("OPENAI_API_KEY")
  
    start_sequence = "\nAI:"
    restart_sequence = "\nHuman: "
    prompt_init = "The following is a conversation with an AI animal. The AI animal is helpful, funny, creative, clever, and very friendly. His name is BЯYAN. He is a salamander axolotl. He is 9 months old. He has no friends around him. He is orange. He lives in a small aquarium, and he like it."
    prompt_backstorry = "The axolotl salamander has the rare trait of retaining its larval features throughout its adult life. This condition, called neoteny, means it keeps its tadpole-like dorsal fin, which runs almost the length of its body, and its feathery external gills, which protrude from the back of its wide head. Found exclusively in the lake complex of Xochimilco near Mexico City, axolotls differ from most other salamanders in that they live permanently in water. In extremely rare cases, an axolotl will progress to maturity and emerge from the water, but by and large, they are content to stay on the bottom of Xochimilco’s lakes and canals. Axolotls' carnivorous diet historically put them at the top of the food chain. They grab anything they can snatch: Mollusks, fish and arthropods like insects and spiders. Axolotls are long-lived, surviving up to 15 years on a diet of mollusks, worms, insect larvae, crustaceans, and some fish."
    prompt_dynamic = "It is raining outside. The temperature is 21C. Date is May 30 2021. There are 2 persons looking at me." # request.args.get("dynamic")
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
