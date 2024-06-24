import google.generativeai as genai
import scratchattach as scratch
import threading
import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_request():
    data = request.json
    # Process data as needed
    return 'OK'

if __name__ == '__main__':
    app.run(port=8080)

# constants
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SESSION_ID = os.getenv("SESSION_ID")
CHARS = (
    [""] * 9
    + [" "]
    + [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "`",
        "~",
        "-",
        "=",
        ".",
        "/",
        ";",
        "'",
        "[",
        "]",
        "\\",
        "|",
        "}",
        "{",
        ":",
        "?",
        ">",
        "<",
        "_",
        "+",
        ")",
        "(",
        "*",
        "&",
        "^",
        "%",
        "$",
        "#",
        "@",
        "!",
        "\n",
    ]
)

# scratch setup
session = scratch.Session(SESSION_ID, username="SupKittyMeow")
conn = session.connect_cloud("967781599")

# gemini setup
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

genai.configure(api_key=GOOGLE_API_KEY)


def encode(data):
    newData = ""
    for letter in str.lower(data):
        try:
            newData = newData + str(CHARS.index(letter) + 1)
        except:
            pass
    return newData


def decode(data):
    newData = ""
    i = 0
    while i < len(data):
        if i % 2 == 1:
            fullNumber = str(data[i - 1]) + str(data[i])
            fullNumber = fullNumber.replace(" ", "")

            try:
                newData = newData + CHARS[int(fullNumber.replace(".", "")) - 1]
            except:
                pass

        i += 1

    return str.lower(newData)


def returnToScratch(content, player):
    conn.set_var("Response", player + "." + content[: 255 - len(player)])
    print("Sent!")


def generate(content, player):
    context = [
        {
            "role": "user",
            "parts": [
                {
                    "text": "System prompt: Limit your response to"
                    + str(255 - len(player))
                    + "characters. Respond understood if you got it."
                }
            ],
        },
        {"role": "model", "parts": [{"text": "Understood."}]},
    ]

    chat = model.start_chat(history=context)

    response = chat.send_message(
        content,
        generation_config=genai.GenerationConfig(max_output_tokens=255 - len(player)),
    )  # this max length will not actually matter because tokens are not characters, but it gives a small limit that might help a little bit.

    returnToScratch(encode(response.text), player)


previousQuestion = scratch.get_var("967781599", "Question")
while True:
    currentQuestion = scratch.get_var("967781599", "Question")
    if currentQuestion == None or currentQuestion[len(currentQuestion) - 1] == ".":
        currentQuestion = previousQuestion
    elif currentQuestion != previousQuestion:
        print("Received!")
        previousQuestion = currentQuestion
        splitQuestion = currentQuestion.split(".")
        thread = threading.Thread(generate(decode(splitQuestion[1]), splitQuestion[0]))
        thread.start()
