FROM python:3.11

WORKDIR /app/

ENV INSTALL_DEV=true
RUN apt update
RUN apt install -y python3-pip
RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY ./app/pyproject.toml ./app/poetry.lock* /app/
RUN poetry lock
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY ./app /app
ENV PYTHONPATH=/app

CMD ["python3", "app/reloader.py"]
