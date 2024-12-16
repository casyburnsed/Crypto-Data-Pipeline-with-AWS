# Crypto-Data-Pipeline-with-AWS

What is this?
This is a project I created to demonstrate how to fetch, process, and analyze real-time cryptocurrency market data using the CoinGecko API and AWS services. In this project, I fetch data, store it in an AWS S3 bucket, query it using AWS Athena, and visualize the results with Python.

The goal of this project is to showcase my skills in Python programming, data analysis, cloud computing with AWS, and SQL-based querying using Athena.

Skills I’m Demonstrating:
1. API Integration
- I used the CoinGecko API to fetch live cryptocurrency data and converted the JSON response into a structured pandas DataFrame.
2. Data Processing and Storage
- I cleaned and structured the data for analysis, saved it to a CSV file, and uploaded the file to an AWS S3 bucket using boto3.
3. Cloud Computing with AWS
- I connected to AWS services using Python SDKs (boto3 and pyathena).
- I created an external table in AWS Athena to query data stored in S3.
- I wrote SQL queries to extract meaningful insights from the data.
4. Data Analysis and Visualization
- I used Python and SQL to analyze cryptocurrency trends.
- I visualized the results with a horizontal bar chart using Matplotlib to make the data more accessible and easy to understand.
5. Error Handling
- I implemented error handling for API requests, S3 uploads, and Athena queries to make sure the project runs smoothly and handles unexpected issues.

Why I Built This Project:
I created this project as a way to integrate multiple technologies and demonstrate my ability to:
1. Work with APIs and manage live data.
2. Perform data engineering tasks like cleaning, storing, and querying data.
3. Use cloud platforms like AWS for scalable data processing and analysis.
4. Present data visually to communicate insights effectively.
