from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_event_sources as event_sources,
    aws_iam as iam,
    core
)


class ComputeStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, db, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fn = _lambda.Function(self, "MyFunction",
                              runtime=_lambda.Runtime.PYTHON_3_8,
                              handler="index.handler",
                              function_name="CWEventUpdater",
                              code=_lambda.Code.from_asset("src"),
                              retry_attempts=1
                              )

        fn.add_event_source(event_sources.DynamoEventSource(db,
                                                            starting_position=_lambda.StartingPosition.TRIM_HORIZON,
                                                            retry_attempts=1
                                                            ))

        fn.role.add_to_policy(iam.PolicyStatement(actions=[
            "events:DeleteRule",
            "events:EnableRule",
            "events:PutRule",
            "events:PutTargets",
            "events:RemoveTargets",
        ],
            resources=["*"],
            effect=iam.Effect.ALLOW
        ))

        target_lambda = _lambda.Function(self, "tgtLambda",
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         handler="index.handler",
                                         function_name="TargetLambda",
                                         code=_lambda.Code.from_inline("""def handler(event, context):
                                  print(event)
                              """),
                                         retry_attempts=1
                                         )

        
        fn.role.add_to_policy(iam.PolicyStatement(actions=[
            "lambda:AddPermission",
            "lambda:RemovePermission",
        ],
            resources=[target_lambda.function_arn],
            effect=iam.Effect.ALLOW
        ))

        # fn.add_permission()
