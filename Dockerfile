FROM python:buster as base

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

FROM base as development

CMD ["python", "-u", "main.py"]

FROM base as release

COPY . .

CMD ["python", "-u", "main.py"]