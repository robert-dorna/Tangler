FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY docs/ ./docs/
COPY tangle.yaml ./
COPY tangle.py ./
CMD [ "python", "./tangle.py", "server" ]
EXPOSE 8000