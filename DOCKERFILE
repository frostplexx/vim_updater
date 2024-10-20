FROM python:3.9-slim

WORKDIR /app

COPY server.py .
COPY update_vimrc.sh .

EXPOSE 8080

CMD ["python", "server.py"]
