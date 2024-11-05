FROM python:3.10-alpine

WORKDIR /app/

COPY ../requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ../ /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]