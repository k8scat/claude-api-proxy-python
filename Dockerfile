FROM python:3.8-slim
LABEL maintainer="K8sCat <k8scat@gmail.com>"

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
