import os
from flask import Flask, request
import google.generativeai as genai
import scratchattach as scratch
import threading

# Constants
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SESSION_ID = os.getenv("SESSION_ID")
CHARS = (
    [""] * 9
    + [" "]
    + [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
        "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6",
        "7", "8", "9", "0", "`", "~", "-", "=", ".", "/", ";", "'", "[", "]", "\\", "|",
        "}", "{", ":", "?", ">", "<", "_", "+", ")", "(", "*", "&", "^", "%", "$", "#",
        "@", "!", "\n"
    ]
)

# Scratch setup
session = scratch.Session(SESSION_ID, username="SupKittyMeow")
conn = session.connect_cloud("967781599")

# Gemini setup
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
genai.configure(api_key=GOOGLE_API_KEY)

# Flask app setup
app = Flask(__name__)

@app.route('/dummy', methods=['GET'])
def dummy_endpoint():
    return 'Server is running'

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
    )
    returnToScratch(encode(response.text), player)

if __name__ == '__main__':
    app.run(port=8080)
