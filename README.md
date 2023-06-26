# NewsInfluencePrediction
This desktop application scrapes headlines and shortcuts of news every given interval (default 15 mins) and uses the ML model to score them with points between -100 (very negative) and 100 (very positive), displaying all the important pieces of information. The score is based on the prediction of how the news will impact the market price of the company, with which it concern. The scope of companies is limited to the 20 biggest Polish companies from the wig20 index (06/2023). The application provides an option for the user to correct a score introducing a human-in-the-loop mechanism, thanks to which, the model keeps learning on the user feedback. The motivation for the project was to create a tool to make daily stock analysis faster and simpler.

Used technologies: Python, Jupyter Notebook, Tkinter, BeautifulSoup, Keras, Scikit-Learn, Matplotlib

## Encountered problems:
- The biggest problem was the amount of data used for model training because of this, the model doesn't capture all subtle dependencies in this NLP problem, the solution to this was introducing a human-in-the-loop mechanism
- Another issue was the same average across batches, which made the model predict the same value over all the samples, the solution was to decrease the batches size, deepen the model and add batchload normalization layers

## Potential developments:
- Feature of choosing the scope of companies that should be tracked
- Feature of saving provided predictions and news so that users can go back to them
- Feature that allows user to change interval from interface
- Model development, bigger embeddings can be used, and/or more data could be provided for the training
- User interface can be updated so that it would be more visually attractive

## Usage:
After running the app, first what you will see after a few seconds is the window with potential news:
![image](https://github.com/NGala540/NewsInfluencePrediction/assets/109106650/d1426096-cd41-44e6-b845-c75a9930f36f)
On the top (1) you can see the headline of the app telling which news is displayed right now and how many of them were scrapped in these 15 minutes, below (2) there is a text box displaying all information about the news (in Polish), including a shortcut of the news and score. Further down (3) there are buttons to switch between scrapped news, and finally (4) there is a box to provide feedback for the model and changed score of the news.

Where there was no news in the past 15 minutes you will see "NO NEWS IN PAST 15 MINUTES" in the text box, when new news is provided you will hear a system sound and see this on the bar:
![image](https://github.com/NGala540/NewsInfluencePrediction/assets/109106650/c8250634-4352-4c74-9178-ab293e9d0be7)


data scrapped from: https://www.biznesradar.pl/

embeding file: http://publications.it.p.lodz.pl/2016/word_embeddings/

stock data: https://stooq.com/db/h/

