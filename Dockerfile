FROM python

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
