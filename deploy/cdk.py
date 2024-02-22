import os
import pathlib

from aws_cdk import App, Stack
from aws_cdk import Environment
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from constructs import Construct


ROOT_DIR = pathlib.Path(__file__).parent.resolve()


class TemplateApiDeploymentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import the default VPC
        vpc = ec2.Vpc.from_lookup(self, f"{construct_id}Vpc", is_default=True)

        # Create an ECS cluster
        cluster = ecs.Cluster(self, f"{construct_id}Cluster", vpc=vpc)

        # Create an ECR repository (optional if you want to push images manually)
        ecr_repository = ecr.Repository(self, f"{construct_id}Repository")

        # Define the task definition with a single container
        task_definition = ecs.FargateTaskDefinition(self, f"{construct_id}TaskDef")
        container = task_definition.add_container(
            f"{construct_id}Container",
            # Use an image from ECR or DockerHub
            image=ecs.ContainerImage.from_ecr_repository(ecr_repository),
            # Specify memory and CPU
            memory_limit_mib=512,
            cpu=256,
        )
        container.add_port_mappings(ecs.PortMapping(container_port=80))

        # Create a Fargate service
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            f"{construct_id}Service",
            cluster=cluster,
            task_definition=task_definition,
            public_load_balancer=True,
        )


app = App()
account = os.getenv("CDK_DEFAULT_ACCOUNT")
region = os.getenv("CDK_DEFAULT_REGION")
print(f"Deploying TemplateAPI stack in {account}:{region}")
env = Environment(account=account, region=region)
TemplateApiDeploymentStack(app, construct_id="TemplateApi", env=env)
app.synth()
