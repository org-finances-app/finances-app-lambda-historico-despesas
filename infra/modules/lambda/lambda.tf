resource "aws_lambda_function" "lambda" {
  function_name    = var.lambda_name
  handler          = var.handler
  runtime          = var.runtime
  filename         = data.archive_file.code.output_path
  source_code_hash = data.archive_file.code.output_base64sha256
  role             = var.role_arn
  layers           = [aws_lambda_layer_version.lambda_layer.arn]
  timeout          = var.timeout
  memory_size      = var.memory_size

  environment {
    variables = var.variables
  }
}

data "archive_file" "code" {
  type        = "zip"
  source_dir  = "${var.source_code_path}"
  excludes    = ["venv"]
  output_path = "${path.module}/code.zip"
}