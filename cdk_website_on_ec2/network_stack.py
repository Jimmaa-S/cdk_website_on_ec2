from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class NetworkStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC with public and private subnets across two AZs
        self.vpc = ec2.Vpc(self, "Vpc",
            max_azs=2,  # Default is all AZs in region
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    cidr_mask=24
                ),
            ]
        )
