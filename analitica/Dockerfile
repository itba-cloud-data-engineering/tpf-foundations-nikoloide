FROM jupyter/scipy-notebook
ENV JUPYTER_TOKEN=itba
ENV PASSWORD=pass
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
VOLUME /notebook
WORKDIR /notebook  