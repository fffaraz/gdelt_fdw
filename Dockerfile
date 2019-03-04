FROM postgres:11.2
RUN pip install Pyrseas && pgxn install multicorn
