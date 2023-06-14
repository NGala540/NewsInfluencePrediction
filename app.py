# TODO: Human in the loop
# TODO: exe file
# TODO: work in background
from tkinter import *
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from app_functions import *
import joblib


def next_news(idx, news):
    idx[0] += 1
    box_head["text"] = f"News no. {idx[0]+1}/{len(news)}"
    box_body.delete("1.0", END)
    box_body.insert("1.0", print_article(news[idx[0]], model, token))
    if idx[0]+1 == len(news):
        b1["state"] = "disabled"


def render_box(idx, news):
    box_head["text"] = f"News no. {idx[0]+1}/{len(news)}"
    box_head.pack()
    box_body.insert("1.0", print_article(news[idx[0]], model, token))
    box_body.pack(side=TOP, fill=X)
    b1["command"] = lambda: next_news(idx, news)
    b1.pack()


model = joblib.load('model.pkl')
token = joblib.load('tokenizer.joblib')

root = Tk()
root.geometry("600x340")
box_body = Text(root, width=15, height=10, wrap=WORD, spacing3=6)
box_head = Label(root)
b1 = Button(root, text="Next")

companies_scope = ['ASSECO-POLAND', "ALE", "ALIOR-BANK", "CD-PROJEKT", "CYFROWY-POLSAT",
                   "DNP", "JSW-JASTRZEBSKA-SPOLKA-WEGLOWA", "KGHM", "KRUK", "KETY","LPP",
                   "MBANK", "ORANGE", "PCO", "PEKAO", "PGE", "PKN-ORLEN", "PKO", "PZU", "SPL"]


def job_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        temp = is_current(event.retval)
        idx = [0]
        render_box(idx, temp)

# TODO: correct appearence of new chunk of news
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.add_job(scrapper, "interval", seconds=20, args=[companies_scope])
    scheduler.add_job(scrapper, "date", args=[companies_scope])
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    root.mainloop()



