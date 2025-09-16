FROM python:3.12

WORKDIR /foam

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ["chmod", "+x", "./run.sh"]
CMD ["./run.sh"]