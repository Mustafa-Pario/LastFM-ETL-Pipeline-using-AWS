import json
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')

BUCKET_NAME = 's3-to-store-lastfm-data'


def lambda_handler(event, context):

    try:
        # Log full incoming event (for debugging)
        print("Full Event:", json.dumps(event))

        # Extract event detail safely
        detail = event.get('detail', {})

        # -------------------------------
        # FIX: Support Last.fm structure
        # -------------------------------
        albums = (
            detail.get('albums') or
            detail.get('top_albums', {})
                  .get('topalbums', {})
                  .get('album', [])
        )

        print("Extracted albums:", json.dumps(albums, indent=2))

        # Validate data
        if not albums:
            print("No album data found in event")
            return {
                'statusCode': 400,
                'body': json.dumps('No album data received')
            }

        # Generate partitioned S3 path
        now = datetime.utcnow()

        key = (
            f"input/{uuid.uuid4().hex}.json"
            # f"spotify/raw/"
            # f"year={now.year}/month={now.month}/day={now.day}/"
            # f"{uuid.uuid4().hex}.json"
        )

        # Prepare payload
        payload = {
            "ingestion_time": now.isoformat(),
            "record_count": len(albums),
            "data": albums
        }

        # Store in S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(payload),
            ContentType='application/json'
        )

        print(f"Data successfully saved to S3: {key}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": "Success",
                "records_stored": len(albums),
                "s3_key": key
            })
        }

    except Exception as e:
        print("Error occurred:", str(e))

        return {
            'statusCode': 500,
            'body': json.dumps({
                "error": str(e)
            })
        }
