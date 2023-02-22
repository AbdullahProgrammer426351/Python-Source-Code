import pyttsx3

converter = pyttsx3.init()

converter.setProperty('rate', 150)
converter.setProperty('volume', 0.7)
names = ["Rahul", "Nishant", "Harry"]
for name in names:
    converter.say(f"Shoutout to {name}")
    print(f"Shoutout to {name}")
    converter.runAndWait()