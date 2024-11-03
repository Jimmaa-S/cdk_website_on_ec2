from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds
from constructs import Construct

class ServerStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define a security group for the web servers
        web_sg = ec2.SecurityGroup(self, "WebServerSG",
            vpc=vpc,
            description="Allow HTTP traffic",
            allow_all_outbound=True
        )
        web_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP traffic")

        # Launch EC2 instances in public subnets
        for i in range(2):  # Two instances in two availability zones
            ec2.Instance(self, f"WebServer{i + 1}",
                instance_type=ec2.InstanceType("t2.micro"),
                machine_image=ec2.MachineImage.latest_amazon_linux(),
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                security_group=web_sg,
            )

        # Define a security group for the RDS instance to allow traffic from the web servers
        rds_sg = ec2.SecurityGroup(self, "RDSSG", vpc=vpc, description="Allow traffic from web servers")
        rds_sg.add_ingress_rule(web_sg, ec2.Port.tcp(3306), "Allow MySQL access from web servers")

        # Create an RDS instance in private subnets with the defined security group
        rds_instance = rds.DatabaseInstance(self, "RDSInstance",
            engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_28),
            instance_type=ec2.InstanceType("t2.micro"),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
            multi_az=False,
            allocated_storage=20,
            database_name="MyDatabase",
            security_groups=[rds_sg],  # Apply the RDS security group here
        )
