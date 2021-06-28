import json
import os
import subprocess
import time
from pathlib import Path

import pytest
from google import pubsub_v1
from google.pubsub_v1 import PushConfig, Subscription

PUBSUB_PROJECT = "msm-groupdata-datalake-dev"
PUBSUB_HOSTPORT = "localhost:8085"
CLOUDFUNCTION_HOSTPORT = "http://localhost:8080"


class TestIntegration:
    @pytest.fixture(autouse=True, scope="class")
    def env(self):
        os.environ["PUBSUB_EMULATOR_HOST"] = PUBSUB_HOSTPORT
        os.environ["PUBSUB_PROJECT_ID"] = PUBSUB_PROJECT

    @pytest.fixture(scope="class")
    def publisher(self):
        return pubsub_v1.PublisherClient()

    @pytest.fixture(scope="class")
    def subscriber(self):
        return pubsub_v1.SubscriberClient()

    @pytest.fixture(scope="class")
    def test_payload(self) -> bytes:
        return json.dumps({"foo": "bar"}).encode('utf8')

    @pytest.fixture(scope="class")
    def dummy_cloud_function(self):
        function_source = Path(__file__).parent.parent / "cloud_function/main.py"
        cmd = f"""functions-framework --signature-type http --target main --source {function_source} --debug"""
        ps_proc = subprocess.Popen(
            cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        # Give the server time to start
        time.sleep(1)

        # check it hasnt terminated
        assert not ps_proc.poll(), ps_proc.stdout.read().decode("utf-8")

        yield

        ps_proc.terminate()
        print(ps_proc.stdout.read().decode("utf-8"))

    @pytest.fixture(scope="class")
    def pubsub_emulator(self):
        """
        This is a generic pubsub emulator fixture.
        No topics or subscriptions
        """
        # project must be valid, but no resources are used
        cmd = f"""gcloud beta emulators pubsub start --project={PUBSUB_PROJECT} --host-port={PUBSUB_HOSTPORT}"""
        ps_proc = subprocess.Popen(
            cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        # Give the server time to start
        time.sleep(1)

        # check it hasnt terminated
        assert not ps_proc.poll(), ps_proc.stdout.read().decode("utf-8")

        yield

        ps_proc.terminate()

    @pytest.fixture(scope="class")
    def pubsub_topic(self, publisher, pubsub_emulator) -> str:
        topic_path = publisher.topic_path(PUBSUB_PROJECT, "dummy_topic")

        # publisher.delete_topic(topic=topic_path)
        topic = publisher.create_topic(name=topic_path)

        yield topic.name

        publisher.delete_topic(topic=topic.name)

    @pytest.fixture(autouse=True)
    def pubsub_subscription(
        self,
        dummy_cloud_function,  # needs to be up before create subscription
        publisher,
        subscriber,
        pubsub_topic,
    ) -> str:
        subscription_path = subscriber.subscription_path(PUBSUB_PROJECT, "dummy_sub")

        subscription = subscriber.create_subscription(
            request=Subscription(
                dict(
                    name=subscription_path,
                    topic=pubsub_topic,
                    push_config=PushConfig(push_endpoint=CLOUDFUNCTION_HOSTPORT),
                )
            )
        )

        yield

        subscriber.delete_subscription(subscription=subscription.name)

    def test_pubsub_to_cloud_function(
        self, pubsub_topic, test_payload, publisher
    ):
        # first we test that the table gets created
        response = publisher.publish(
            topic=pubsub_topic, messages=[dict(data=test_payload)]
        )
        print(response)
        time.sleep(2)
        with open('request_payloads.jsonl', 'rb') as f:
            assert f.read() == test_payload

