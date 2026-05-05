import json
import boto3
import csv
import io
from urllib.parse import unquote_plus

s3 = boto3.client('s3')


def lambda_handler(event, context):

    try:
        print("EVENT RECEIVED:", json.dumps(event))

        # -------------------------------
        # 1. Get file from S3 trigger
        # -------------------------------
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        print(f"Reading file from S3: {key}")

        # -------------------------------
        # 2. Read JSON from S3
        # -------------------------------
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        json_data = json.loads(content)

        print("RAW JSON:", json.dumps(json_data, indent=2))

        # -------------------------------
        # 3. FIX: Ensure correct structure
        # -------------------------------
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        if "body" in json_data and isinstance(json_data["body"], str):
            json_data = json.loads(json_data["body"])

        # -------------------------------
        # 4. Extract data
        # -------------------------------
        records = json_data.get("data", [])

        if not records:
            print("No data found inside JSON structure")
            return {
                'statusCode': 400,
                'body': 'No data found in JSON file'
            }

        # -------------------------------
        # 5. Convert JSON → CSV
        # -------------------------------
        csv_buffer = io.StringIO()

        headers = [
            "name",
            "artist_name",
            "playcount",
            "rank",
            "url",
            "image_url"
        ]

        writer = csv.DictWriter(csv_buffer, fieldnames=headers)
        writer.writeheader()

        for item in records:

            artist_name = item.get("artist", {}).get("name")

            rank = item.get("@attr", {}).get("rank")

            image_url = ""
            for img in item.get("image", []):
                if img.get("size") == "extralarge":
                    image_url = img.get("#text")

            writer.writerow({
                "name": item.get("name"),
                "artist_name": artist_name,
                "playcount": item.get("playcount"),
                "rank": rank,
                "url": item.get("url"),
                "image_url": image_url
            })

        # -------------------------------
        # 6. Save CSV to output folder
        # -------------------------------
        output_key = key.replace("input/", "output/").replace(".json", ".csv")

        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )

        print(f"CSV SUCCESSFULLY SAVED: {output_key}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": "CSV transformation successful",
                "output_file": output_key,
                "records_processed": len(records)
            })
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }