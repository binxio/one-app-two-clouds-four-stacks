## 02-static-website
A simple S3 static website

## Assignment
Do the following:

- read `templates/static-website.yaml`
- read [AWS::S3::Bucket](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html)
- read `aws s3 help`
- deploy the stack
- get the stack outputs
- copy the files from `html` to the s3 bucket
- get the `BucketWebsiteUrl` of the static website using `make describe`
- View the static website using the `BucketWebsiteUrl`
- Alter the text of `index.html`
- Update the index.html file in the bucket
- View the changes
- Delete all files from the bucket
- Delete the stack