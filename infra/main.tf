terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "sa-east-1"
}

locals {
    lambda_name = "lambda-historico-despesa"
}


module "iam_role" {
  source = "./modules/lambda_role"
  
  lambda_name = local.lambda_name
  role_name = "${local.lambda_name}-role"
  policy_name = "${local.lambda_name}-policy"
}

module "lambda" {
  source = "./modules/lambda"
  
  lambda_name = local.lambda_name
  role_arn = module.iam_role.role_arn
  memory_size = 1024
  timeout = 600

  depends_on = [
    module.iam_role
  ]
}

resource "aws_cloudwatch_event_rule" "daily_rule" {
  name                = "daily-run-${local.lambda_name}"
  description         = "Executa a lambda diariamente para atualizar o histórico de despesas"
  schedule_expression = "cron(0 4 * * ? *)" # todo dia 01:00 BRT
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_rule.name
  target_id = "lambda_target"
  arn       = module.lambda.lambda_arn
}

resource "aws_lambda_permission" "permission" {
  statement_id  = "AllowExecutionFromCloudWatchEvents"
  action        = "lambda:InvokeFunction"
  function_name = local.lambda_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_rule.arn
}


