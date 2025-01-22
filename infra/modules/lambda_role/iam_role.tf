resource "aws_iam_role" "iam_role" {
  name                = var.role_name
 
  managed_policy_arns = [
    aws_iam_policy.iam_policy.arn
  ]

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}