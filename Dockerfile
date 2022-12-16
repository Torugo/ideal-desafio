FROM python:3.10-bullseye

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
# watch app' files
ENV FLASK_DEBUG=true
ENV FLASK_ENV=development

EXPOSE 5050

RUN chmod u+x ./entrypoint.sh
# running Flask as a module
CMD ["sh", "-c", "sleep 5 \ 
    # ! run init only the first time you launch the stack and when the migrations folder do not exist yet
    && ./entrypoint.sh"]