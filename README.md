# Twitter Sentiment Analysis
This project uses NLP to analyse tweets related to the top trending subjects on twitter, in order to understand public opinion.

## Technologies
This project uses:
* [twint](https://github.com/twintproject/twint) for scraping tweets
* [kafka-python](https://kafka-python.readthedocs.io/en/master/#) for sending the tweets over kafka 
* [pyspark](https://hub.docker.com/r/jupyter/pyspark-notebook) for collecting the tweets, and aggregating them
* [vaderStatement](https://github.com/cjhutto/vaderSentiment) for Sentiment Analysis
* [matplotlib](https://matplotlib.org/) for plotting the data

## Running the docker container
To run this container, from the root of the project (The location of docker-compose.yml file), run:
```
docker-compose up --build
```

Check the logs of the jupyter service, to get the token and open jupyterlab
Under work, open "Sentiment Analysis" notebook, and execute the cells in order 

## Information
This proejct is prepared by Elie Yaacoub, for the "Spark and Python for Big Data" course @ EPITA 