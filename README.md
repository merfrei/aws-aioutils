### AWS Python Utils

It is only S3 utilities for now

```python
from aws.s3 import Bucket

async def main():
    bucket = Bucket('mybucket')
    await bucket.upload_file('/path/to/my/localfile.txt', 'localfile_in_bucket.txt')
```
