FROM python:latest
WORKDIR /usr/src/app
COPY pyproject.toml ./
RUN pip install poetry
RUN poetry install --no-cache --no-interaction --without=dev
COPY tangler tangler/
COPY spaces spaces/
COPY main.py ./
COPY spaces.yml ./
STOPSIGNAL SIGINT
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000
CMD [ "poetry", "run", "flask", "--app", "/usr/src/app/main.py", "--debug", "run" ]
EXPOSE 8000
