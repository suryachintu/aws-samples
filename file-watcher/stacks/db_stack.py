from attr import s
from aws_cdk import (
    aws_dynamodb as dynamodb,
    core,
    aws_kinesis as kinesis
)


class DatabaseStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # stream = kinesis.Stream(self, "dbStream", stream_name="DyanamoDbStream", encryption=kinesis.StreamEncryption.UNENCRYPTED)

        self.db = dynamodb.Table(self, "cfg_table",
                            partition_key=dynamodb.Attribute(
                                name="id", type=dynamodb.AttributeType.STRING),
                            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                            removal_policy=core.RemovalPolicy.DESTROY,
                            table_name="file_cfg",
                            # kinesis_stream=stream,
                            stream=dynamodb.StreamViewType.NEW_AND_OLD_IMAGES
                            )

    @property
    def db_table(self):
        return self.db
