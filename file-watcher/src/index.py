import boto3


def handler(event, context):
    # Record Inserted
    print(event)
    record = event['Records'][0]['dynamodb']
    event_type = event['Records'][0]["eventName"]

    cfg_id = record["Keys"]["id"]["S"]

    if event_type == "INSERT":
        # a. Create a new cloudwatch event rule
        client = boto3.client('events')
        # print("Creating CloudWatch")
        response = client.put_rule(
            Name=cfg_id,
            ScheduleExpression='rate(1 minute)',
            State='DISABLED',
            Description=f'File Watcher Cloud Watch Event Rule for Cfg Id: {cfg_id}',
        )
        # b. Add Target as Lambda function
        response = client.put_targets(
            Rule=cfg_id,
            Targets=[
                {
                    'Id': 'lambda_target',
                    'Arn': 'arn:aws:lambda:us-east-2:036140352936:function:TargetLambda',
                }])
        # c. Add Persmission for Cloud watch event to Invoke Lambda Function
        client = boto3.client('lambda')

        response = client.add_permission(
            FunctionName='arn:aws:lambda:us-east-2:036140352936:function:TargetLambda',
            StatementId=f'{cfg_id}_LambdaInvokePermission',
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com',
            SourceArn=f'arn:aws:events:us-east-2:036140352936:rule/{cfg_id}',
        )
        # d. Enable Cloud Watch Event Rule
        client = boto3.client('events')
        response = client.enable_rule(
            Name=cfg_id
        )
    elif event_type == "MODIFY":
        pass
    else:
        # delete cloudwatch event rule
        client = boto3.client('events')
        response = client.remove_targets(
            Rule=cfg_id,
            Ids=[
                'lambda_target',
            ]
        )
        response = client.delete_rule(
            Name=cfg_id
        )
        # remove permission from target lambda

        client = boto3.client('lambda')

        response = client.remove_permission(
            FunctionName='arn:aws:lambda:us-east-2:036140352936:function:TargetLambda',
            StatementId=f'{cfg_id}_LambdaInvokePermission',
        )
