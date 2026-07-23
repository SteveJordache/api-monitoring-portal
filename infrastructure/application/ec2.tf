data "aws_ami" "ubuntu" {
  most_recent = true

  owners = [
    "099720109477"
  ]

  filter {
    name = "name"

    values = [
      "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"
    ]
  }

  filter {
    name = "virtualization-type"

    values = [
      "hvm"
    ]
  }

  filter {
    name = "architecture"

    values = [
      "x86_64"
    ]
  }
}

resource "aws_instance" "application" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.application.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2.name

  associate_public_ip_address = true

  user_data = templatefile("${path.module}/user-data.sh", {
    project_name       = var.project_name
    aws_region         = var.aws_region
    backup_bucket_name = var.backup_bucket_name
    ecr_repository_url = aws_ecr_repository.application.repository_url
  })

  user_data_replace_on_change = true

  root_block_device {
    volume_type           = "gp3"
    volume_size           = var.root_volume_size
    encrypted             = true
    delete_on_termination = true
  }

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  depends_on = [
    aws_iam_role_policy_attachment.ec2_application,
    aws_iam_role_policy_attachment.ec2_ssm,
    aws_route_table_association.public
  ]

  tags = {
    Name = "${var.project_name}-application"
  }
}
