#!/usr/bin/env python3

from aws_cdk import core

from cwlambda.cwlambda_stack import CwlambdaStack


app = core.App()
CwlambdaStack(app, "cwlambda", env={'region': 'us-east-2'})

app.synth()
