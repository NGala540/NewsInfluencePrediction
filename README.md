# NewsInfluencePrediction
This desktop application scrapes headlines and shortcuts of news every given interval (default 15 mins) and uses the ML model to score them with points between -100 (very negative) and 100 (very positive), displaying all the important pieces of information. The score is based on the prediction of how the news will impact the market price of the company, with which it concerns. The scope of companies is limited to the 20 biggest Polish companies from the wig20 index (06/2023). The application provides an option for the user to correct a score introducing a human-in-the-loop mechanism, thanks to which, the model keeps learning on the user feedback.

Used technologies: Python, Jupyter Notebook, Tkinter, BeautifulSoup, Keras, Scikit-Learn, Matplotlib

## Encountered problems:
- The biggest problem was the amount of data used for model training because of this model doesn't capture all subtle dependencies in this NLP problem, the solution to this was introducing a human-in-the-loop mechanism
- Another issue was the same average across batches, which made the model predict the same value over all the samples, the solution was to decrease the batches size, deepen the model and add batchload normalization layers


## Potential developments:
- Application can be developed to provide the user with the availability to choose the scope of companies that should be tracked
- There is potential development in the model, where bigger embeddings can be used and/or more data could be provided for the model
- User interface can be updated so that it would be more visually attractives

data scrapped from: https://www.biznesradar.pl/

embeding file: http://publications.it.p.lodz.pl/2016/word_embeddings/

stock data: https://stooq.com/db/h/

The motivation of the project was to creat a tool to make daily stock analysis faster and simpler, application also will provide real-time noticing of new news.

