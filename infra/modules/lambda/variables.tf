variable "lambda_name" {
    type = string
}

variable "role_arn" {
    type = string
}

variable "runtime" {
    type = string
    default = "python3.11"
}

variable "handler" {
    type = string
    default = "lambda_function.lambda_handler"
}

variable "source_code_path" {
    type = string
    default = "../app"
}

variable "timeout" {
    type = number
    default = 30
}

variable "variables" {
    type = map(string)
    default = {}
}

variable "memory_size" {
    type = number
    default = 128
}