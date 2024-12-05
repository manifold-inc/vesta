FROM python:3.10 
RUN pip install vesta python-dotenv pycoingecko pytz
COPY main.py .
ENTRYPOINT ["python", "./main.py"] 
