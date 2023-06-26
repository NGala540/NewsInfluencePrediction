from tkinter import *
import tkinter.messagebox
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from app_functions import *


def box_actualization(idx, news):
    """
    Actualize Headline of the box with news counter and body with all news data
    :param idx: index of current displaying news
    :param news: data frame of news
    """
    box_body.delete("1.0", END)
    if len(news) > 0:
        box_head["text"] = f"News no. {idx[0] + 1}/{len(news)}"
        box_body.insert("1.0", print_article(news.iloc[idx[0]]))
    else:
        box_body.insert("1.0", "NO NEWS IN PAST 15 MINUTES")


def next_news(idx, news):
    """
    Moves index to next news, checking if next button should be active
    :param idx: index of current displaying news
    :param news: data frame of news
    """
    idx[0] += 1
    box_actualization(idx, news)
    b2["state"] = "normal"
    if idx[0]+1 == len(news):
        b1["state"] = "disabled"


def previous_news(idx, news):
    """
    Moves index to previous news,
    checks if previous button should be active
    :param idx: index of current displaying news
    :param news: data frame of news
    """
    idx[0] -= 1
    box_actualization(idx, news)
    b1["state"] = "normal"
    if idx[0] == 0:
        b2["state"] = "disabled"


def take_score(idx, news):
    """
    Takes score from entry box,
    checks if it is in proper range,
    actualize model and updates news data frame
    :param idx: index of current displaying news
    :param news: data frame of news
    """
    score = ent_score.get()
    try:
        if int(score) > 100:
            score = 100
        elif int(score) < -100:
            score = -100
        model_actualization(score, news.iloc[idx[0]])
        news.loc[idx[0], 'Score'] = score
        box_actualization(idx, news)
    except ValueError:
        print("Value should be a number")
    except IndexError:
        print("No news to assign a score to")
    finally:
        ent_score.delete(0, END)


def render_box(idx, news):
    """
    Organize and creates first display,
    handles functions to button assignment and its status
    :param idx: index of current displaying news
    :param news: data frame of news
    """
    box_actualization(idx, news)
    box_head.pack()
    box_body.pack()

    b1["command"] = lambda: next_news(idx, news)
    if len(news) > 1:
        b1["state"] = "normal"
    else:
        b1["state"] = "disabled"
    b1.pack(side=RIGHT, padx=10)

    b2["command"] = lambda: previous_news(idx, news)
    b2["state"] = "disabled"
    b2.pack(side=LEFT, padx=10)

    button_frame.pack(pady=7)
    ent_score.pack()
    b3["command"] = lambda: take_score(idx, news)
    b3.pack(pady=3)


def job_listener(event):
    """
    Listener of a web scrap event,
    take scrapped news, filter current ones and adds score to them,
    set index of current news to 0,
    render box
    """
    if event.exception:
        print('The job crashed :(')
    else:
        current_news = is_current(event.retval)
        news_score = score_calculate(current_news)
        if len(news_score) != 0:
            show_message()
        idx = [0]
        render_box(idx, news_score)


def show_message():
    """
    display message when new news appear
    """
    tkinter.messagebox.showinfo("Let's make some money!",  "There are some new news for you")
    root.deiconify()
    root.attributes('-topmost', 1)
    root.attributes('-topmost', 0)


def on_closing():
    """
    save the model if it was changed
    """
    if changed is True:
        joblib.dump(model, 'model.pkl')
    root.destroy()


# Scope of handles companies
SCOPE = ["ASSECO-POLAND", "ALE", "ALIOR-BANK", "CD-PROJEKT", "CYFROWY-POLSAT",
         "DNP", "JSW-JASTRZEBSKA-SPOLKA-WEGLOWA", "KGHM", "KRUK", "KETY","LPP",
         "MBANK", "ORANGE", "PCO", "PEKAO", "PGE", "PKN-ORLEN", "PKO", "PZU", "SPL"]

# main root of app declaration
root = Tk()
root.geometry("600x340")

# widgets creation
box_body = Text(root, width=150, height=10, wrap=WORD, spacing3=6)
box_head = Label(root)
button_frame = Frame(root)
b1 = Button(button_frame, text="Next")
b2 = Button(button_frame, text="Previous")
ent_score = Entry(master=root, width=10)
b3 = Button(master=root, text="Update Score")

# job scheduler declaration
scheduler = BackgroundScheduler()
scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
# parameter minutes decide how frequent scrapper should run
scheduler.add_job(scrapper, "interval", minutes=15, args=[SCOPE])
scheduler.add_job(scrapper, "date", args=[SCOPE])
scheduler.start()

# save model and shut down the scheduler when exiting the app
root.protocol("WM_DELETE_WINDOW", on_closing)
atexit.register(lambda: scheduler.shutdown())
root.mainloop()
