provider "aws" {
  region                  = "us-east-1"  # Specify any region, LocalStack simulates all regions
  access_key              = "dummy-access-key"
  secret_key              = "dummy-secret-key"
  skip_credentials_check = true
  skip_metadata_api_check = true
  endpoints {
    apigateway             = "http://localhost:4567"
    cloudformation         = "http://localhost:4581"
    cloudwatch             = "http://localhost:4582"
    dynamodb               = "http://localhost:4569"
    es                     = "http://localhost:4578"
    firehose               = "http://localhost:4573"
    iam                    = "http://localhost:4593"
    kinesis                = "http://localhost:4568"
    lambda                 = "http://localhost:4574"
    route53                = "http://localhost:4580"
    redshift               = "http://localhost:4577"
    s3                     = "http://localhost:4572"
    ses                    = "http://localhost:4579"
    sns                    = "http://localhost:4575"
    sqs                    = "http://localhost:4576"
    ssm                    = "http://localhost:4583"
    stepfunctions          = "http://localhost:4585"
  }
}

# Example: Create an S3 bucket in LocalStack
resource "aws_s3_bucket" "example_bucket" {
  bucket = "my-example-bucket"
}
