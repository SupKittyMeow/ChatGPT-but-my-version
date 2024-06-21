import google.generativeai as genai
import scratchattach as scratch
import threading
import os

# constants
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SESSION_ID = os.getenv('SESSION_ID')
chars = [
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
      newData = newData + str(chars.index(letter) + 1)
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
        newData = newData + chars[int(fullNumber.replace(".", "")) - 1]
      except:
        pass

    i += 1
  return newData

def returnToScratch(content, player):
  conn.set_var('Response', content[:255 - len(player)] + '.' + player)
  print('Sent!')

def generate(content, player):
    response = model.generate_content(content)
    print(response.text)
    returnToScratch(encode(response.text), player)

previousQuestion = scratch.get_var('967781599', 'Question')
while True:
   currentQuestion = scratch.get_var('967781599', 'Question')

   if currentQuestion != previousQuestion:
        try:
          print('Received!')
          previousQuestion = currentQuestion
          splitQuestion = currentQuestion.split('.')
          thread = threading.Thread(generate(decode(splitQuestion[1]), splitQuestion[0]))
          thread.start()
        except Exception as e:
          print('Error: ' + e)