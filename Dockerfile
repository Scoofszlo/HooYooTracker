FROM python:3.10-alpine
WORKDIR /app

RUN pip install uv==0.6.6 --no-cache-dir

COPY uv.lock pyproject.toml ./
RUN uv pip install -r pyproject.toml --system
COPY hooyootracker ./hooyootracker

EXPOSE 8080

CMD ["python", "-m", "hooyootracker"]
