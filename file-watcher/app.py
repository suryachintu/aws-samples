#!/usr/bin/env python3

from aws_cdk import core

from stacks.db_stack import DatabaseStack
from stacks.compute_stack import ComputeStack

app = core.App()
_db_stack = DatabaseStack(app, "db-stack", env={"region":"us-east-2"})
ComputeStack(app, "compute-stack", _db_stack.db_table , env={"region":"us-east-2"})
app.synth()
