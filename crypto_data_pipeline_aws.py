import requests as re
import pandas as pd
import boto3
from pyathena import connect
import matplotlib.pyplot as plt

# Fetch crypto data from CoinGecko
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "sparkline": False
}

# GET request to Coin Gecko API
response = re.get(url, params=params)
if response.status_code == 200: 
    # JSON response and convert to pandas DataFrame
    data = response.json()
    dataframe = pd.DataFrame(data)

    # Build data frame 
    dataframe = dataframe[["id", "symbol", "name", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"]]
    
    # Save data frame to CSV 
    dataframe.to_csv("crypto_data.csv", index=False)
    print("Data saved to crypto_data.csv")

else: 
    print(f"Failed to fetch data: {response.status_code}")


# Connecting Amazon S3 bucket
aws_access_key = "access-key"
aws_secret_key = "secret-key"
bucket_name = "crypto-data-bucket"
file_name = "crypto_data.csv"

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# Upload csv file into s3
try:
    s3.upload_file(file_name, bucket_name, file_name)
    print(f"Simulating upload of {file_name} to S3 bucket {bucket_name}")

except Exception as e: 
    print(f"Failed to upload file to S3: {e}")


# Connecting AWS Athena 
s3_staging_dir = f"s3://{bucket_name}/athena-results"
region_name = "us-west-2"

conn = connect(
    aws_access_key_id=aws_access_key, 
    aws_secret_access_key=aws_secret_key,
    s3_staging_dir=s3_staging_dir,
    region_name=region_name
)

# Create AWS Athena Table (SQL)
create_table_query = f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS crypto_data (
    id STRING,
    symbol STRING,
    name STRING, 
    current_price FLOAT,
    market_cap BIGINT,
    total_volume BIGINT,
    price_change_percentage_24h FLOAT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'field.delim' = ','
)
STORED AS TEXTFILE
LOCATION 's3://{bucket_name}/'
TBLPROPERTIES ('has_encrypted_data'='false');
"""
cursor = conn.cursor()
cursor.execute(create_table_query)
print("Athena table 'crypto_data' created successfully.")

# Crypto query
query = """
SELECT name, current_price, market_cap, total_volume
FROM crypto_data
WHERE market_cap > 1000000000
ORDER BY market_cap DESC
LIMIT 10;
"""

cursor.execute(query)
results = cursor.fetchall()

print("Query Results:")
if results:
    for row in results:
        print(row)
else:
    print("No results returned from Athena query")


# Visualizing data with bar chart 
df_results = pd.DataFrame(results, columns=["name", "current_price", "market_cap", "total_volume"])

if not df_results.empty:
    plt.figure(figsize=(10, 6))
    plt.barh(df_results["name"], df_results["market_cap"], color="skyblue")
    plt.xlabel("Market cap (USD)")
    plt.ylabel("Cryptocurrency")
    plt.title("Top Cryptocurrencies by Market Cap")
    plt.gca().invert_yaxis()
    plt.show()

else:
    print("No data available for visualization.")