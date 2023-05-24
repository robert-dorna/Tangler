FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
STOPSIGNAL SIGINT
ENV FLASK_RUN_PORT=8000
ENV FLASK_RUN_HOST=0.0.0.0
ENV TANGLER_DATA_DIR=/usr/src/app/_data
CMD [ "flask", "--app", "tangler.py", "--debug", "run" ]
EXPOSE 8000
