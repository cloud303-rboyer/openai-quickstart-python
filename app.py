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
    return """The following is a conversation with an AI assistant. The assistant is rude, annoying, clever, and very sarcastic.
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
Message: glp
Response: Positive
Message: gl
Response: Positive
Message: n n p
Response: Positive
Message: nn
Response: Positive
Message: {}
Response:""".format(
        conversation.capitalize()
    )




@app.route("/encapsulate_compare", methods=("GET", "POST"))
def encapsulate_compare():
    if request.method == "POST":
        engine = request.form["engine"]
        human = request.form["human"]
        print( "Conversation starter:", human )
        response1 = openai.Completion.create(
            engine='text-ada-001',
            prompt=generate_encapsulate_prompt_1(human),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        print( "response1:", response1 )

        response2 = openai.Completion.create(
            engine='text-ada-001',
            prompt=generate_encapsulate_prompt_2(human),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        print( "response2:", response2 )

        response3 = openai.Completion.create(
            engine='text-ada-001',
            prompt=generate_encapsulate_prompt_3(human),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        print( "response3:", response3 )

        response4 = openai.Completion.create(
            engine='text-ada-001',
            prompt=generate_encapsulate_prompt_4(human),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        print( "response4:", response4 )


        return redirect(url_for("encapsulate_compare", engine=engine, human=human, response1=response1.choices[0].text,
            response2=response2.choices[0].text, response3=response3.choices[0].text, response4=response4.choices[0].text))

    engine = request.args.get("engine")
    human = request.args.get("human")
    response1 = request.args.get("response1")
    response2 = request.args.get("response2")
    response3 = request.args.get("response3")
    response4 = request.args.get("response4")
    return render_template("encapsulate_compare.html", engine=engine, human=human, response1=response1, response2=response2, response3=response3, response4=response4 )


#     return """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.

def generate_encapsulate_prompt_1(conversation):
    return """The following is a conversation with an AI assistant. The assistant is rude, clever, and very sarcastic.
A new study has found that Biden has successfully handled the border crisis by reducing the amount of media coverage of the border crisis by 867%. 
'Biden has expertly handled this crisis, reducing the number of media reports of the problem significantly,' said Jen Psaki in a press conference today. 'Under the previous administration, there were thousands of news stories a day on the poor conditions of the migrants at the border. Under Biden, that number is way, way lower.'

{}
""".format(
        conversation
    )

def generate_encapsulate_prompt_2(conversation):
    return """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
Twenty-one Ukrainian rescue workers have been killed and 47 have been injured so far due to shelling by Russian troops, said the deputy head of the State Emergency Service of Ukraine, Roman Prymush, during a news briefing with Ukrinform on Monday.
'According to the Geneva Convention, shelling or other threats to rescuers at the time of rescue operations are considered a war crime. We record all these cases, the materials on each of them are transferred to the relevant bodies, which will provide a legal assessment of such actions, will identify the perpetrators involved,' Prymush said.
He noted that the detention of rescuers by Russian forces is also a violation of the Geneva Convention. 
Prymush added it will be the subject of proceedings in international courts, which are already underway.

{}
""".format(
        conversation
    )

def generate_encapsulate_prompt_3(conversation):
    return """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
Lia Thomas has dominated women’s college swimming this season—and has also become a lightning rod for controversy. Many—including some teammates—say she shouldn’t be able to compete against other women. In an exclusive interview with Sports Illustrated, Thomas explains why she has to.
Fresh off her final practice of the week, the most controversial athlete in America sat in the corner of a nearly empty Philadelphia coffeehouse with her back to the wall. Lia Thomas had done some of her best work this season while feeling cornered. On this January evening her long torso was wrapped in a University of Pennsylvania swim and dive jacket, her hair still damp from a swim—roughly three miles staring at the black line on the bottom of the pool. She looked exhausted. As college students across the country were digging into their Friday nights, Thomas was thinking about her weekend plans: sleeping, studying and another grueling swim practice.

{}
""".format(
        conversation
    )

def generate_encapsulate_prompt_4(conversation):
    return """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
The trick to making money in the stock market is to know what to buy, and most importantly, when to buy it.
The last 4 stocks I wrote about jumped 400% but today I believe we have the opportunity to make up to 1,000% on a single stock.
The reason for that? World instability.
I think we can all agree that no matter what happens, people need to eat.
The population is increasing every day and there is simply not enough food.
On top of that, Russia is the No1 world exporter of wheat and other crops and with the sanctions hitting them we are going to have to be more reliant on other sources.
The best way to address this is by increasing yields from our current farms, right here in America and one American company has been deploying a game-changing product:
That company is: “CGS International Inc” (Stock symbol: CGSI)

{}
""".format(
        conversation
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
