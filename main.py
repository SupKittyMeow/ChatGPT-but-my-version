import google.generativeai as genai
import scratchattach as scratch
import threading
import os

# constants
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SESSION_ID = os.getenv('SESSION_ID')
CHARS = [
    '', '', '', '', '', '', '', '', '', ' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
    'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '`', '~', '-', '=',
    '.', '/', ';', "'", '[', ']', '\\', '|', '}', '{', '"', ':', '?', '>', '<', '_',
    '+', ')', '(', '*', '&', '^', '%', '$', '#', '@', '!', '¶', '\r'
]

# scratch setup
session = scratch.Session(SESSION_ID, username='SupKittyMeow')
conn = session.connect_cloud('967781599')

# gemini setup
model = genai.GenerativeModel(model_name='gemini-1.5-flash')
genai.configure(api_key=GOOGLE_API_KEY)

def encode(data):
  newData = ''
  for letter in data:
    try:
      newData = newData + str(CHARS.index(letter) + 1)
    except:
      pass
  return newData

def decode(data):
  newData = ''
  i = 0
  while i < len(data):
    if (i % 2 == 1):
      fullNumber = str(data[i - 1]) + str(data[i])
      fullNumber = fullNumber.replace(" ", "")

      try:
        newData = newData + CHARS[int(fullNumber.replace(".", "")) - 1]
      except:
        pass

    i += 1
  return newData

def returnToScratch(content, player):
  conn.set_var('Response', content[:255 - len(player)] + '.' + player)
  print('Sent!')

def generate(content, player):
    parameter = '##PARAMETERS## Ensure that any text you create or modify contains only the following characters: (a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9 0 ~ - = . / ; \' [ ] \\ | } { " : ? > < _ + ) ( * & ^ % $ # @ ! ¶ `) Any character not listed above should not be used. Also, make sure your response is less than ' + str(255 - len(player)) + ' characters. ##CONTENT## '
    response = model.generate_content(parameter + content, generation_config = genai.GenerationConfig( max_output_tokens = 255 - len(player) )) # this max length will not actually matter because tokens are not characters, but it gives a small limit that might help a little bit.
    returnToScratch(encode(response.text), player)

previousQuestion = scratch.get_var('967781599', 'Question')
while True:
   currentQuestion = scratch.get_var('967781599', 'Question')

   if currentQuestion != previousQuestion:
      print('Received!')
      previousQuestion = currentQuestion
      splitQuestion = currentQuestion.split('.')
      thread = threading.Thread(generate(decode(splitQuestion[1]), splitQuestion[0]))
      thread.start()