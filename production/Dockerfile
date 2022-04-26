FROM python:3.8

RUN apt-get -qq update
RUN mkdir app

# Specify working directory
WORKDIR /app
COPY . .

# Install al requirements
RUN pip install --upgrade pip && pip install pip-tools
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh


EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "bot.py" ]

