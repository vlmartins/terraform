variable "users" {
  description = "List of users"
  type = list(object({
    name = string
    email = string
    auth_key = string
  }))
  default = []
}

provider "aws" {
  region  = "sa-east-1"
}
resource "aws_instance" "example" {
  count = length(var.users)

  ami           = "ami-0af6e9042ea5a4e3e"
  instance_type = "t2.micro" //Example instance type, replace with your own

  key_name = aws_key_pair.example[count.index].key_name

  tags = {
    Name = var.users[count.index].name
  }
}

resource "aws_key_pair" "example" {
  count = length(var.users)

  key_name   = var.users[count.index].name
  public_key = var.users[count.index].auth_key
}
