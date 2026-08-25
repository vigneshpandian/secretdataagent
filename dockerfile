FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip && pip install uv

COPY pyproject.toml README.md uv.lock* ./
COPY src ./src

RUN uv pip install --system --no-cache .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "secretdataagent:app", "--host", "0.0.0.0", "--port", "8000"]