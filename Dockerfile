FROM python:3.10 
COPY main.py .
RUN pip install vesta python-dotenv pycoingecko
ENTRYPOINT ["python", "./main.py"] 
