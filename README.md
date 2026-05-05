# LastFM-ETL-Pipeline-using-AWS

## 📌 Project Overview

This project builds a serverless ETL (Extract, Transform, Load) pipeline using the Last.fm API and Amazon Web Services.
It extracts music data, processes it, stores it in a data lake, and enables querying for analytics.

## 🏗️ Architecture

The pipeline follows this flow:

Last.fm API → Python → EventBridge → Lambda (Extract) → S3 (Raw)
→ S3 Event Notification → Lambda (Transform) → S3 (Processed)
→ Glue Crawler → Glue Data Catalog → Athena

## ⚙️ Technologies Used

Python
Amazon EventBridge
AWS Lambda
Amazon S3
AWS Glue
AWS Glue Data Catalog
Amazon Athena

## 🔄 How It Works

1. Data Extraction
- Python script uses Last.fm API (lastfmapi)
- Fetches user listening data (tracks, artists, etc.)

2. Scheduling
- EventBridge triggers the pipeline on a schedule (hourly/daily)

4. Raw Data Storage
- Lambda stores raw JSON data in S3 bucket

6. Event Trigger
- S3 event notification triggers another Lambda

8. Data Transformation
- Cleans and converts JSON → CSV/Parquet
- Stores processed data in another S3 bucket

10. Data Cataloging
- Glue Crawler scans processed data
- Creates tables in Glue Data Catalog

12. Data Analysis
- Athena queries data using SQL
- Generates insights like top artists and trends

## 🏁Conclusion

This project demonstrates how to build a real-world ETL pipeline using AWS services and external APIs. It provides a scalable solution for music data analytics.

