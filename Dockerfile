FROM postgres:11.2
RUN easy_install pgxnclient && pgxn install multicorn
