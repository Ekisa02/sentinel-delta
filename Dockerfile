FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "sentinel_delta.main:app", "--host", "0.0.0.0", "--port", "8000"]
