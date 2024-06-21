import google.generativeai as genai
import scratchattach as scratch
import threading
import os

# constants
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SESSION_ID = os.getenv('SESSION_ID')

# scratch setup
session = scratch.Session(SESSION_ID, username='SupKittyMeow')
conn = session.connect_cloud('967781599')

# gemini setup
model = genai.GenerativeModel('gemini-1.5-flash')
genai.configure(api_key=GOOGLE_API_KEY)

def decode(content):
  newContent = content.split('.')
  return scratch.Encoding.decode(newContent[0]), newContent[1]

def returnToScratch(content, player):
  conn.set_var('Response', content + '.' + player)

def generate(content, player):
    response = model.generate_content(content)
    returnToScratch(scratch.Encoding.encode(response), player)

previousQuestion = conn.get_var('Question')
while True:
   currentQuestion = conn.get_var('Question')

   if currentQuestion != previousQuestion:
      decoded = decode(currentQuestion)
      thread = threading.Thread(generate(decoded[0], decoded[1]))
      thread.start()