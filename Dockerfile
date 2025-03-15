FROM python:3.10-slim
WORKDIR /app

RUN pip install poetry==2.1.1 --no-cache-dir

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --without dev --no-root
COPY hooyootracker ./hooyootracker

EXPOSE 8080

CMD ["python", "-m", "hooyootracker"]
