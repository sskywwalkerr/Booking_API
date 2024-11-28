#FROM python:3.8.3
#
#RUN mkdir -p /usr/src/app/
#WORKDIR /usr/src/app/
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#RUN pip install --upgrade pip
#RUN pip install fastapi uvicorn redis aiohttp fastapi_utils
#
#COPY . /usr/src/app/

FROM python:3.8.3

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt



COPY . .

EXPOSE 8000

ENV HOST 0.0.0.0

CMD ["fastapi","run","src","--port","8000","--host","0.0.0.0"]
