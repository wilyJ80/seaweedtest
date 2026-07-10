import asyncio
import aioboto3

session = aioboto3.Session()

async def main():
    async with session.client(
        "s3",
        endpoint_url="http://localhost:8333",
        aws_access_key_id="admin",
        aws_secret_access_key="admin123",
        region_name="us-east-1",
    ) as s3:

        await s3.put_object(
            Bucket="test",
            Key="hello.txt",
            Body=b"hello world",
        )

        obj = await s3.get_object(
            Bucket="test",
            Key="hello.txt",
        )

        print(await obj["Body"].read())

asyncio.run(main())
