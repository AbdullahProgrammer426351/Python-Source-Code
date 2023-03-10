import time
from plyer import notification
while True:
    notification.notify(
        title = "**Hey! Don't Forget to drink water",
        message ="Drinking at least 8 glasses is necessary for your health",
        timeout= 10
        )
    time.sleep(60*60)