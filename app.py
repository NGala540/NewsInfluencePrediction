# TODO: Human in the loop
# TODO: exe file
# TODO: work in background
from tkinter import *
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from ContinuousWebScrapper import *
import joblib

root = Tk()
canvas1 = Canvas(root, width=600, height=300)
canvas1.pack()
model = joblib.load('model.pkl')
token = joblib.load('tokenizer.joblib')

# TODO: correct display
h = Scrollbar(root, orient='horizontal')
h.pack(side=BOTTOM, fill=X)
v = Scrollbar(root)
v.pack(side=RIGHT, fill=Y)
t = Text(root, width=15, height=15, wrap=NONE,
         xscrollcommand=h.set,
         yscrollcommand=v.set)

# TODO: compaies from wig20
companies_scope = ['PLAYWAY', "LPP", "GPW", "KGHM", "DINOPL"]


def job_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        temp = is_current(event.retval)
        for i in temp:
            t.insert(END, print_article(i, model, token))
            t.pack(side=TOP, fill=X)
            h.config(command=t.xview)
            v.config(command=t.yview)


# TODO: Scrapping to new line
# TODO: don't scrap already scrapped
# TODO: scheduler doesn't run on app start
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.add_job(scrapper, "interval", seconds=60, args=[companies_scope])
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    root.mainloop()

