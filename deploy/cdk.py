import os
import pathlib

from aws_cdk import (
    App,
    Stack,
    Duration,
    Environment,
    RemovalPolicy,
    aws_logs as logs,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
)
from constructs import Construct


PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
ACCOUNT = os.getenv("CDK_DEFAULT_ACCOUNT")
REGION = os.getenv("CDK_DEFAULT_REGION")


class TemplateApiDeploymentStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Import the default VPC
        vpc = ec2.Vpc.from_lookup(self, f"{id}Vpc", is_default=True)

        # Create an ECS cluster
        cluster = ecs.Cluster(
            self,
            f"{id}Cluster",
            cluster_name=f"{id}Cluster",
            vpc=vpc,
        )

        # Log group for the container logs
        log_group = logs.LogGroup(
            self,
            f"{id}LogGroup",
            log_group_name=f"{id}LogGroup",
            retention=logs.RetentionDays.SIX_MONTHS,
            removal_policy=RemovalPolicy.DESTROY,
        )

        task_image_options = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_asset(str(PROJECT_ROOT)),
            container_name=f"{id}Container",
            container_port=80,
            log_driver=ecs.LogDriver.aws_logs(
                stream_prefix=f"{id}",
                log_group=log_group,
            ),
        )

        # Create a Fargate service
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            f"{id}ALBFargateService",
            cpu=256,
            memory_limit_mib=512,
            assign_public_ip=True,
            public_load_balancer=True,
            cluster=cluster,
            task_image_options=task_image_options,
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
TemplateApiDeploymentStack(app, "TemplateApi", env=env)
app.synth()
