import pyttsx3
# You have to install pyttsx3 library when you have to convert text into python
# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties (optional)
#engine.setProperty('rate', 150)    # Speed of speech
#engine.setProperty('rate', 200)  # Higher values for faster speech
#engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use voices[1].id for a female voice
# Text to be converted to speech
text = "Hello, welcome to the text to speech conversion demo. hi Farhat "
# Convert text to speech
engine.say(text)

# Wait for the speech to finish
engine.runAndWait()
