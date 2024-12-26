FROM python:3.11-slim

RUN mkdir /my_booking

WORKDIR /my_booking

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#EXPOSE 8000
#
#CMD ["uvicorn", "api.db.main:app", "--host", "0.0.0.0", "--port", "8000"]