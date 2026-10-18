FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements-prod.txt
ENV PORT=8000
CMD ["sh","-c","gunicorn -b 0.0.0.0:$PORT wsgi:app"]
