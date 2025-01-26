FROM python:3.12.8-bookworm

COPY Requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./

CMD ["python","main.py"]