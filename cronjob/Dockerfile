FROM python:3.8-slim

COPY ./script ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "datachecker.py"]