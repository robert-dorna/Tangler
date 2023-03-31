FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY docs/ ./docs/
COPY tangler.yaml ./
COPY tangler.py ./
STOPSIGNAL SIGINT
CMD [ "python", "./tangler.py", "server" ]
EXPOSE 8000