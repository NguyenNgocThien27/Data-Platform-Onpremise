FROM hadoop-base:latest

COPY nodemanager-init.sh nodemanager-init.sh 

RUN chmod +x nodemanager-init.sh 

EXPOSE 8042
# ENTRYPOINT [ "/bin/bash" ]
CMD [ "./nodemanager-init.sh" ]