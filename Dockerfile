FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /src
WORKDIR /src

EXPOSE 8000

ENTRYPOINT ["python", "fstr_rest_api/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]