FROM jupyter/pyspark-notebook

# COPY pyspark /usr/local/spark/bin
USER root
RUN sudo apt update && apt install -y netcat
RUN pip install kafka-python
RUN pip install spark-nlp==4.0.1
RUN pip install vaderSentiment
# RUN sudo apt install -y nc
# RUN pip install confluent-kafka
# RUN pip install --force-reinstall pyspark==2.4.6
