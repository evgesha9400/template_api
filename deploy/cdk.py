import os
import pathlib

from aws_cdk import App, Stack, Duration
from aws_cdk import Environment
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from constructs import Construct


PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
ACCOUNT = os.getenv("CDK_DEFAULT_ACCOUNT")
REGION = os.getenv("CDK_DEFAULT_REGION")


class TemplateApiDeploymentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import the default VPC
        vpc = ec2.Vpc.from_lookup(self, f"{construct_id}Vpc", is_default=True)

        # Create an ECS cluster
        cluster = ecs.Cluster(self, f"{construct_id}Cluster", cluster_name=f"{construct_id}Cluster", vpc=vpc)

        task_image_options = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_asset(str(PROJECT_ROOT)),
            container_name=f"{construct_id}Container",
            container_port=80
        )

        # Create a Fargate service
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            f"{construct_id}ALBFargateService",
            assign_public_ip=True,
            cluster=cluster,
            memory_limit_mib=512,
            cpu=256,
            task_image_options=task_image_options,
            public_load_balancer=True,
            desired_count=1,
            health_check_grace_period=Duration.seconds(60),
        )

        # Configure the health check path and response codes
        fargate_service.target_group.configure_health_check(
            path="/healthcheck",
            healthy_http_codes="200",
            healthy_threshold_count=2,
            interval=Duration.seconds(10),
            timeout=Duration.seconds(5),
            unhealthy_threshold_count=2,
        )


app = App()
env = Environment(account=ACCOUNT, region=REGION)
TemplateApiDeploymentStack(app, construct_id="TemplateApi", env=env)
app.synth()
