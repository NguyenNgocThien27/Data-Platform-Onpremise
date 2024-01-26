FROM hadoop-base:latest

COPY resourcemanager-init.sh resourcemanager-init.sh 

RUN chmod a+x resourcemanager-init.sh 

EXPOSE 8088
# ENTRYPOINT [ "/bin/bash" ]
CMD [ "./resourcemanager-init.sh" ]