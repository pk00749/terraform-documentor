# S3 模块输出

output "bucket_id" {
  description = "S3 存储桶 ID"
  value       = aws_s3_bucket.main.id
}

output "bucket_arn" {
  description = "S3 存储桶 ARN"
  value       = aws_s3_bucket.main.arn
}

output "bucket_domain_name" {
  description = "S3 存储桶域名"
  value       = aws_s3_bucket.main.bucket_domain_name
}

output "bucket_regional_domain_name" {
  description = "S3 存储桶区域域名"
  value       = aws_s3_bucket.main.bucket_regional_domain_name
}

output "bucket_hosted_zone_id" {
  description = "S3 存储桶托管区域 ID"
  value       = aws_s3_bucket.main.hosted_zone_id
}

output "bucket_region" {
  description = "S3 存储桶区域"
  value       = aws_s3_bucket.main.region
}

output "bucket_versioning_status" {
  description = "存储桶版本控制状态"
  value       = aws_s3_bucket_versioning.main.versioning_configuration[0].status
}
