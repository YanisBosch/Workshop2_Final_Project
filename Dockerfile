FROM python:3.12.8-slim-bookworm

COPY Requirements.txt ./
RUN pip install --no-cache-dir -r Requirements.txt

COPY main.py ./

CMD ["python","main.py"]