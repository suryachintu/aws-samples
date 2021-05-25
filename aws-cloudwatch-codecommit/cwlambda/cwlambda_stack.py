from aws_cdk import (
    core,
    aws_events as events,
    aws_lambda as _lambda,
    aws_events_targets as targets,
    aws_iam as iam
)


class CwlambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_role = iam.Role(self, "LambdaRole",
                           role_name="CCLambdaRole",
                           assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))

        my_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        my_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))

        cc_rule = events.Rule(self, "CWEventRule",
                              description="Code Commit rule",
                              event_pattern=events.EventPattern(
                                  detail={
                                      "event": ["pullRequestMergeStatusUpdated"],
                                      "destinationReference": [
                                          "refs/heads/master",
                                          "refs/heads/develop"
                                      ]
                                  },
                                  detail_type=["CodeCommit Pull Request State Change"],
                                  source=["aws.codecommit"],
                              ),
                              rule_name="CodeCommitRule",
                              )

        handler = _lambda.Function(
            self,
            "MyLambdaFunction",
            code=_lambda.Code.from_inline("""def handler(event, context):
            print(event)
            return "Success"
            """),
            handler="index.handler",
            role=my_role,
            runtime=_lambda.Runtime.PYTHON_3_8
        )

        cc_rule.add_target(targets.LambdaFunction(handler))