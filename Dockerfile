FROM python:3.9-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./bot /app/bot
COPY ./requirements.txt /app
COPY ./pytube /app/pytube
RUN pip install -r requirements.txt
CMD ["python", "bot/app.py"]