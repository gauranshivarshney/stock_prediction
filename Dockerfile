FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "stock_prediction_main.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=3"]