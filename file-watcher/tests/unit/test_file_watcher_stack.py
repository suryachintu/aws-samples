import json
import pytest

from aws_cdk import core
from file-watcher.file_watcher_stack import FileWatcherStack


def get_template():
    app = core.App()
    FileWatcherStack(app, "file-watcher")
    return json.dumps(app.synth().get_stack("file-watcher").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
