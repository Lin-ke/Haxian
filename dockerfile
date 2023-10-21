FROM python:3.9-slim
WORKDIR /Haxian
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
# flask environment
ENV FLASK_APP=autoapp.py
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=14535"]