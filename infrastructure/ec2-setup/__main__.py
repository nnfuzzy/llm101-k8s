import pulumi
import pulumi_aws as aws
from starter_script import user_data

# Get the default VPC
default_vpc = aws.ec2.get_vpc(default=True)

# Create a new security group
security_group = aws.ec2.SecurityGroup("instance-security-group",
    description="Allow SSH access",
    vpc_id=default_vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],
    )],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        )
    ]
)



eip = aws.ec2.Eip("ec2-eip",
    vpc=True,  # Specify if this Elastic IP is for a VPC
    tags={
        "Name": "PermanentIP"
    }
)


# Create EC2 instance with spot pricing
instance = aws.ec2.Instance("ec2-instance",
    instance_type="t3a.xlarge",
    vpc_security_group_ids=[security_group.id],
    user_data=user_data,
    ami="ami-0a628e1e89aaedf80",
    associate_public_ip_address=True,
    key_name="pulumi2025",
    # Spot instance configuration
    instance_market_options={
        "marketType": "spot",
        "spotOptions": {
            "maxPrice": "0.10",
            "spotInstanceType": "one-time",
        },
    },
    root_block_device={
    "volumeSize": 50,  # Size in GiB
    "volumeType": "gp3",  # General Purpose SSD (GP3 is cost-efficient)
    "deleteOnTermination": True  # Automatically delete the volume when the instance is terminated    
    },
    tags={
        "Name": "SpotInstance-Dev",
        "Environment": "Development"
    }
)

# Associate Elastic IP with the instance
eip_association = aws.ec2.EipAssociation("ec2-eip-association",
    instance_id=instance.id,
    allocation_id=eip.id
)

# Export the instance's public IP and DNS
pulumi.export('public_ip', instance.public_ip)
pulumi.export('public_dns', instance.public_dns)