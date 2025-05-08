#!/bin/bash

# LocalStack が起動するのを待つ
echo "Waiting for LocalStack to start..."
until aws --endpoint-url=http://localstack:4566 dynamodb list-tables; do
  echo "Waiting for DynamoDB..."
  sleep 5
done

# scraping_data テーブルの作成
echo "Creating table 'scraping_data'..."
aws --endpoint-url=http://localstack:4566 dynamodb create-table \
  --table-name scraping_data \
  --attribute-definitions \
    AttributeName=data_id,AttributeType=S \
  --key-schema \
    AttributeName=data_id,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

# 初期データの挿入
echo "Inserting initial data into 'scraping_data'..."
aws --endpoint-url=http://localstack:4566 dynamodb put-item \
  --table-name scraping_data \
  --item \
    '{"data_id": {"S": "penelope"}, "title": {"S": "タイトル"}, "page_url": {"S": "ページURL"}}'

echo "Setup completed."
