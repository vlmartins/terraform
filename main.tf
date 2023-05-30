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

resource "aws_security_group" "devs2blu_sg" {
  name        = "devs2blu_sg"
  description = "grupo-de-seguranca"
  
  # Permite o tráfego nas portas 80, 22, 8069 e 443 de qualquer endereço IP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  } 

  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
   egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "devs2blu" {
  count = length(var.users)

  ami           = "ami-06fce8d0a4e8889ca"
  instance_type = "t2.micro" //Example instance type, replace with your own

  key_name = aws_key_pair.devops[count.index].key_name
  vpc_security_group_ids = [aws_security_group.devs2blu_sg.id]
  tags = {
    Name = var.users[count.index].name
  }
}

resource "aws_key_pair" "devops" {
  count = length(var.users)

  key_name   = var.users[count.index].name
  public_key = var.users[count.index].auth_key

}

output "instance_details" {
  value = { for idx, i in aws_instance.devs2blu : "${var.users[idx].name}:${var.users[idx].email}" => i.public_ip
  } 
  description = "The public IPs and hostnames of the instances"
}