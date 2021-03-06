import sys

import gevent.event
from mock import MagicMock

from rpc_job_process_data import sample_definition
from sample_manager import SampleManager

sys.modules['tendrl.commons.config'] = MagicMock()

from tendrl.commons.flows.exceptions import FlowExecutionFailedError
from tendrl.commons.manager.rpc_job_process import EtcdRPC
from tendrl.commons.manager.rpc_job_process import RpcJobProcessThread
import uuid


class Test_EtcdRpc(object):
    def test_constructor(self, monkeypatch):
        def mock_config_get(package, parameter):
            if parameter == "etcd_port":
                return 2379
            elif parameter == "etcd_connection":
                return "0.0.0.0"

        manager = SampleManager("aa22a6fe-87f0-45cf-8b70-2d0ff4c02af6")
        monkeypatch.setattr(manager._config, 'get', mock_config_get)
        syncJobThread = RpcJobProcessThread(manager)
        server = EtcdRPC(syncJobThread, MagicMock())

        assert server.syncJobThread._manager.integration_id == \
            "aa22a6fe-87f0-45cf-8b70-2d0ff4c02af6"

    def test_stop(self):
        assert True

    def test_process_job_positive(self, monkeypatch):
        def mock_config_get(package, parameter):
            if parameter == "etcd_port":
                return 2379
            elif parameter == "etcd_connection":
                return "0.0.0.0"

        manager = SampleManager("49fa2adde8a6e98591f0f5cb4bc5f44d")
        monkeypatch.setattr(manager._config, 'get', mock_config_get)
        syncJobThread = RpcJobProcessThread(manager)
        server = EtcdRPC(syncJobThread, MagicMock())

        def mock_uuid4():
            return 'aa22a6fe-87f0-45cf-8b70-2d0ff4c02af6'

        monkeypatch.setattr(uuid, 'uuid4', mock_uuid4)

        def mock_etcd_write(key, value):
            pass

        monkeypatch.setattr(server.etcd_orm.client, 'write', mock_etcd_write)

        def mock_invoke_flow(flow, job, definitions):
            return {"key1": "value1", "key2": "value2"}, "", ""

        monkeypatch.setattr(server, 'invoke_flow', mock_invoke_flow)

        input_raw_job1 = {
            "status": "new",
            "cluster_id": "49fa2adde8a6e98591f0f5cb4bc5f44d",
            "type": "node",
            "parameters": {"Node[]": ['node1', 'node2'],
                           "sds_name": "gluster", "sds_version": "3.2.0",
                           "cluster_id": "mycluster"},
            "run": "tendrl.node_agent.gluster_integration.flows"
                   ".import_cluster.ImportCluster",
        }

        server.validate_flow = MagicMock(return_value=True)
        raw_job, executed = server._process_job(
            input_raw_job1,
            "9a9604c0-d2a6-4be0-9a82-262f10037a8f",
            "node"
        )

        assert executed
        assert raw_job['status'] == "finished"
        assert raw_job['request_id'] == "/clusters/" \
            "49fa2adde8a6e98591f0f5cb4bc5f44d/_jobs/" \
            "tendrl.node_agent.gluster_integration.flows.import_cluster" \
            ".ImportCluster_aa22a6fe-87f0-45cf-8b70-2d0ff4c02af6"

        input_raw_job2 = {
            "status": "processing", "sds_type": "generic",
            "cluster_id": "49fa2adde8a6e98591f0f5cb4bc5f44d",
            "errors": {}, "attributes": {"_raw_params": "ls"},
            "message": "Executing command",
            "type": "node",
            "object_type": "generic",
            "flow": "ExecuteCommand"
        }

        manager = SampleManager("49fa2adde8a6e98591f0f5cb4bc5f44d")
        monkeypatch.setattr(manager._config, 'get', mock_config_get)
        syncJobThread = RpcJobProcessThread(manager)
        server = EtcdRPC(syncJobThread, MagicMock())

        def mock_etcd_write(key, value):
            pass

        monkeypatch.setattr(server.etcd_orm.client, 'write', mock_etcd_write)

        def mock_invoke_flow(flow, job):
            return {"key1": "value1", "key2": "value2"}, ""

        monkeypatch.setattr(server, 'invoke_flow', mock_invoke_flow)

        raw_job, executed = server._process_job(
            input_raw_job2,
            "9a9604c0-d2a6-4be0-9a82-262f10037a8f",
            "node"
        )
        assert not executed

        input_raw_job3 = {
            "status": "new", "sds_type": "gluster",
            "cluster_id": "49fa2adde8a6e98591f0f5cb4bc5f44d",
            "errors": {}, "attributes": {"_raw_params": "ls"},
            "message": "Executing command",
            "type": "sds",
            "object_type": "generic",
            "flow": "ExecuteCommand"
        }

        manager = SampleManager("49fa2adde8a6e98591f0f5cb4bc5f44d")
        monkeypatch.setattr(manager._config, 'get', mock_config_get)
        syncJobThread = RpcJobProcessThread(manager)
        server = EtcdRPC(syncJobThread, MagicMock())

        def mock_etcd_write(key, value):
            pass

        monkeypatch.setattr(server.etcd_orm.client, 'write', mock_etcd_write)

        def mock_invoke_flow(flow, job):
            return {"key1": "value1", "key2": "value2"}, ""

        monkeypatch.setattr(server, 'invoke_flow', mock_invoke_flow)

        raw_job, executed = server._process_job(
            input_raw_job3,
            "9a9604c0-d2a6-4be0-9a82-262f10037a8f",
            "node"
        )
        assert not executed

    def test_process_job_finished(self, monkeypatch):
        def mock_config_get(package, parameter):
            if parameter == "etcd_port":
                return 2379
            elif parameter == "etcd_connection":
                return "0.0.0.0"

        manager = SampleManager("49fa2adde8a6e98591f0f5cb4bc5f44d")
        monkeypatch.setattr(manager._config, 'get', mock_config_get)
        syncJobThread = RpcJobProcessThread(manager)
        server = EtcdRPC(syncJobThread, MagicMock())

        def mock_uuid4():
            return 'aa22a6fe-87f0-45cf-8b70-2d0ff4c02af6'

        monkeypatch.setattr(uuid, 'uuid4', mock_uuid4)

        def mock_etcd_write(key, value):
            pass

        monkeypatch.setattr(server.etcd_orm.client, 'write', mock_etcd_write)

        def mock_invoke_flow(flow, job):
            raise FlowExecutionFailedError("Flow Execution failed")

        monkeypatch.setattr(server, 'invoke_flow', mock_invoke_flow)

        input_raw_job1 = {
            "status": "new", "sds_type": "generic",
            "cluster_id": "49fa2adde8a6e98591f0f5cb4bc5f44d",
            "errors": {}, "attributes": {"_raw_params": "ls"},
            "type": "node",
            "message": "Executing command",
            "object_type": "generic",
            "run": "ExecuteCommand"
        }
        server.validate_flow = MagicMock(return_value=False)
        raw_job, executed = server._process_job(
            input_raw_job1,
            "9a9604c0-d2a6-4be0-9a82-262f10037a8f",
            "node")
        assert raw_job['status'] == "finished"

    def test_extract_flow_details(self, monkeypatch):
        def mock_config_get(package, parameter):
            if parameter == "etcd_port":
                return 2379
            elif parameter == "etcd_connection":
                return "0.0.0.0"

        manager = SampleManager("49fa2adde8a6e98591f0f5cb4bc5f44d")
        monkeypatch.setattr(manager._config, 'get', mock_config_get)
        syncJobThread = RpcJobProcessThread(manager)
        server = EtcdRPC(syncJobThread, MagicMock())

        flow_name = "tendrl.gluster_integration.flows." \
                    "create_volume.CreateVolume"

        definition = sample_definition

        result = server.extract_flow_details(flow_name, definition)

        assert result[0] == [
            'tendrl.gluster_integration.objects.volume.atoms.create'
        ]

        flow_name = 'tendrl.gluster_integration.objects.' \
                    'Volume.flows.start_volume.StartVolume'

        result = server.extract_flow_details(flow_name, definition)

        assert result[0] == [
            'tendrl.gluster_integration.objects.volume.atoms.start'
        ]


class TestRpcJobProcessThread(object):
    def test_etcdthread_constructor(self):
        manager = SampleManager("49fa2adde8a6e98591f0f5cb4bc5f44d")
        user_request_thread = RpcJobProcessThread(manager)
        assert isinstance(user_request_thread._manager, SampleManager)
        assert isinstance(user_request_thread._complete, gevent.event.Event)
        assert isinstance(user_request_thread._server, EtcdRPC)

    def test_etcdthread_stop(self):
        manager = SampleManager("49fa2adde8a6e98591f0f5cb4bc5f44d")
        user_request_thread = RpcJobProcessThread(manager)
        assert not user_request_thread._complete.is_set()

        user_request_thread.stop()

        assert user_request_thread._complete.is_set()

    def test_etcdthread_run(self, monkeypatch):
        manager = SampleManager("49fa2adde8a6e98591f0f5cb4bc5f44d")
        user_request_thread = RpcJobProcessThread(manager)

        user_request_thread._complete.set()
        user_request_thread._run()

        user_request_thread2 = RpcJobProcessThread(manager)

        user_request_thread2.EXCEPTION_BACKOFF = 1

        def mock_server_run():
            raise Exception

        monkeypatch.setattr(user_request_thread._server,
                            'run', mock_server_run)

        assert True
