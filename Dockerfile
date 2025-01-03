FROM python:3.9-slim

EXPOSE 80
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip3 config  set global.index-url http://mirrors.aliyun.com/pypi/simple/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt --trusted-host mirrors.aliyun.com
COPY ./app /code/app

WORKDIR /code/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
# uvicorn main:app --host '0.0.0.0' --port 8089 --reload
# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]