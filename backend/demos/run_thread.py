from app.core.application import Application
import time

app = Application()

app.start()

time.sleep(4000)

app.stop()