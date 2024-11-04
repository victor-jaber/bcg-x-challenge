FROM python:3.9
WORKDIR /app
COPY . .
RUN mkdir -p /app/log
RUN pip install --no-deps -r requirements.txt
RUN python -m nltk.downloader stopwords
CMD ["python", "api.py"]
