FROM umihico/aws-lambda-selenium-python:latest
# ソースのコピー
COPY src/ ./
# ライブラリのインストール
RUN pip install -r requirements.txt -t .

<<<<<<< HEAD
CMD [ "main.pene" ]
=======
CMD [ "lambda_function.scraping_lambda" ]
>>>>>>> 5707c40 (no message)
