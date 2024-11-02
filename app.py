#!/usr/bin/env python3
import os

import aws_cdk as cdk
from cdk_website_on_ec2.network_stack import NetworkStack
from cdk_website_on_ec2.server_stack import ServerStack

app = cdk.App()

# Instantiate the NetworkStack
network_stack = NetworkStack(app, "NetworkStack")

# Instantiate the ServerStack and pass the VPC from NetworkStack
ServerStack(app, "ServerStack", vpc=network_stack.vpc)

app.synth()

