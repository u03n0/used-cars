FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501

CMD ["streamlit", "run", "frontend/app.py"]
