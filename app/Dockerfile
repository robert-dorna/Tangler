FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
COPY tangler.yaml /usr/local/bin
STOPSIGNAL SIGINT
ENV FLASK_RUN_PORT=8000
ENV FLASK_RUN_HOST=0.0.0.0
CMD [ "flask", "--app", "tangler.py", "--debug", "run" ]
EXPOSE 8000

# WORKDIR /app
# COPY src/ ./src/
# COPY docs/ ./docs/
# COPY tangler.yaml ./
# COPY tangler.py ./
# CMD [ "bash" ]
# CMD [ "python", "./tangler.py", "server" ]