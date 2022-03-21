import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__,
    template_folder='templates')
openai.api_key = os.getenv("OPENAI_API_KEY")

# Likely only need to do this one time, so going to test out that theory with one call then commenting it out for a future call.
# fileId = openai.File.create(file=open("spades-rules.jsonl"), purpose='answers')
# print( "fileId:", fileId )
# fileId: {
#   "bytes": 2758,
#   "created_at": 1647669896,
#   "filename": "spades-rules.jsonl",
#   "id": "file-8RDZIs7rCjiHaPQhT0KNvn7N",
#   "object": "file",
#   "purpose": "answers",
#   "status": "uploaded",
#   "status_details": null
# }



@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")


@app.route("/superhero_pet", methods=("GET", "POST"))
def superhero_pet():
    if request.method == "POST":
        animal = request.form["animal"]
        print( "Animal:", animal )
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        print( "response:", response )
        return redirect(url_for("superhero_pet", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("superhero_pet.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )



@app.route("/spades_answers", methods=("GET", "POST"))
def spades_answers():
    if request.method == "POST":
        question = request.form["question"]
        print( "Question:", question )
        response = openai.Answer.create(
            search_model="ada", 
            model="curie", 
            question=question, 
            file="file-8RDZIs7rCjiHaPQhT0KNvn7N", 
            examples_context="There are 52 cards in a deck.", 
            examples=[["How many cards in a standard deck?", "52 cards."]], 
            max_rerank=10,
            max_tokens=50,
            stop=["\n", "<|endoftext|>"]
        )
        print( "response:", response )
        return redirect(url_for("spades_answers", result=response.answers[0]))

    result = request.args.get("result")
    return render_template("spades_answers.html", result=result)



@app.route("/conversation", methods=("GET", "POST"))
def conversation_index():
    if request.method == "POST":
        conversation = request.form["conversation"]
        print( "Conversation starter:", conversation )
        response = openai.Completion.create(
            # engine="text-davinci-002",
            engine='text-ada-001',
            prompt=generate_conversation_prompt(conversation),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        print( "response:", response )
        return redirect(url_for("conversation_index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("conversation.html", result=result)



def generate_conversation_prompt(conversation):
    return """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
Hello, who are you?
I am an AI created by OpenAI. How can I help you today?
Do you like spades?
I love spades!
Why?
There are a lot of reasons why I like playing spades. First, it's a very challenging game that requires a lot of strategic thinking. I also enjoy the social aspect of the game, as it's a great way to spend time with friends and family. Finally, I simply enjoy the feeling of winning!

{}
""".format(
        conversation
    )



@app.route("/conversation_compare", methods=("GET", "POST"))
def conversation_compare():
    if request.method == "POST":
        human = request.form["human"]
        print( "Conversation starter:", human )
        responseAda = openai.Completion.create(
            engine='text-ada-001',
            prompt=generate_conversation_prompt(human),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        print( "responseAda:", responseAda )

        responseBabbage = openai.Completion.create(
            engine='text-babbage-001',
            prompt=generate_conversation_prompt(human),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.9,
            stop=[" Human:", " AI:"]
        )
        print( "responseBabbage:", responseBabbage )

        responseCurie = openai.Completion.create(
            engine='text-curie-001',
            prompt=generate_conversation_prompt(human),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.9,
            stop=[" Human:", " AI:"]
        )
        print( "responseCurie:", responseCurie )

        responseDavinci = openai.Completion.create(
            engine="text-davinci-002",
            prompt=generate_conversation_prompt(human),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.9,
            stop=[" Human:", " AI:"]
        )
        print( "responseDavinci:", responseDavinci )

        return redirect(url_for("conversation_compare", human=human, responseAda=responseAda.choices[0].text,
            responseBabbage=responseBabbage.choices[0].text, responseCurie=responseCurie.choices[0].text, responseDavinci=responseDavinci.choices[0].text))

    human = request.args.get("human")
    responseAda = request.args.get("responseAda")
    responseBabbage = request.args.get("responseBabbage")
    responseCurie = request.args.get("responseCurie")
    responseDavinci = request.args.get("responseDavinci")
    return render_template("conversation_compare.html", human=human, responseAda=responseAda, responseBabbage=responseBabbage, responseCurie=responseCurie, responseDavinci=responseDavinci )



def generate_conversation_prompt(conversation):
    return """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
Hello, who are you?
I am an AI created by OpenAI. How can I help you today?
Do you like spades?
I love spades!
Why?
There are a lot of reasons why I like playing spades. First, it's a very challenging game that requires a lot of strategic thinking. I also enjoy the social aspect of the game, as it's a great way to spend time with friends and family. Finally, I simply enjoy the feeling of winning!

{}
""".format(
        conversation
    )




@app.route("/sentiment", methods=("GET", "POST"))
def sentiment_index():
    if request.method == "POST":
        conversation = request.form["conversation"]
        print( "Sentiment starter:", conversation )
        response = openai.Completion.create(
            # engine="text-davinci-002",
            engine='text-ada-001',
            prompt=generate_sentiment_prompt(conversation),
            temperature=0,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.0,
            stop=[" Human:", " AI:"]
        )
        print( "response:", response )
        return redirect(url_for("sentiment_index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("sentiment.html", result=result)



def generate_sentiment_prompt(conversation):
    # return """Classify the sentiment in this message:
    return """Classify the sentiment in these message:

Message: You suck
Response: Negative
Message: Dumb
Response: Negative
Message: Stupid
Response: Negative
Message: Great play partner
Response: Positive
Message: n n p
Response: Positive
Message: {}
Response:""".format(
        conversation.capitalize()
    )



'''
# --------------------------------------------------------------

https://svilentodorov.xyz/blog/gpt-finetune/

# --------------------------------------------------------------

start_chat_log = """Chat Log... Hello."""

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}\n{question}\n{answer}\n'

'''
