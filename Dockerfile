FROM umihico/aws-lambda-selenium-python:latest
# ソースのコピー
COPY src/ ./
# ライブラリのインストール
RUN pip install -r requirements.txt -t .

CMD [ "main.pene" ]