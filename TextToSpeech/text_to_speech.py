from gtts import gTTS
import os

myText = "All the detriment of this world results from a lack of individual ability."

language = 'en'

output = gTTS(text=myText, lang=language, slow=False)

output.save("output.mp3")

os.system("start output.mp3")
