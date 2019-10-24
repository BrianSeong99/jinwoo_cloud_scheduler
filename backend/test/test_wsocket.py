"""
Unit test for websocket
"""
import time
import pytest
from channels.testing import WebsocketCommunicator
import mock
import wsocket
from wsocket.views import WebSSH, UserWebSSH
from user_model.models import UserModel, UserType
from task_manager.models import TaskSettings
from task_manager.executor import TaskExecutor
from .common import MockTaskExecutor, MockWSClient


def mock_stream(_p0, _p1, _p2, **_):
    return MockWSClient()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def testSSHConnect():
    with mock.patch.object(wsocket.views, 'stream', mock_stream):
        communicator = WebsocketCommunicator(WebSSH, "/terminals/?pod=none&shell=/bin/sh")
        connected, _ = await communicator.connect()
        assert connected
        _ = UserModel.objects.create(username='admin', user_type=UserType.ADMIN, uuid='uuid', password='pass',
                                     salt='salt', email='email@email.com', token='my_only_token',
                                     token_expire_time=round(time.time()) + 100)
        _ = await communicator.send_to('admin@my_only_token')
        response = await communicator.receive_from()
        assert response == 'Hello from WebSocket!\n'
        await communicator.send_to('Hello world')
        await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def testSSHConnectAuthFailed():
    with mock.patch.object(wsocket.views, 'stream', mock_stream):
        communicator = WebsocketCommunicator(WebSSH, "/terminals/?pod=none&shell=/bin/sh")
        connected, _ = await communicator.connect()
        assert connected
        _ = UserModel.objects.create(username='admin', user_type=UserType.ADMIN, uuid='uuid', password='pass',
                                     salt='salt', email='email@email.com', token='my_only_token',
                                     token_expire_time=round(time.time()) + 100)
        _ = await communicator.send_to('admin@error_token')
        response = await communicator.receive_from()
        assert response == 'Authentication failed.'
        await communicator.disconnect()


@pytest.mark.asyncio
async def testSSHConnectInvalid():
    communicator = WebsocketCommunicator(WebSSH, "/terminals/?pod=none&shell=/bin/bad-sh")
    connected, _ = await communicator.connect()
    assert connected
    response = await communicator.receive_from()
    assert response == "\nInvalid request."
    await communicator.disconnect()


@pytest.mark.asyncio
async def testUserSSHConnectInvalidReq():
    communicator = WebsocketCommunicator(UserWebSSH, "/user_terminals/")
    connected, _ = await communicator.connect()
    assert connected
    response = await communicator.receive_from()
    assert response == "\nInvalid request."
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def testUserSSHUserOrTaskNotExist():
    communicator = WebsocketCommunicator(UserWebSSH, "/user_terminals/?uuid=2000&token=2000&username=200")
    connected, _ = await communicator.connect()
    assert connected
    response = await communicator.receive_from()
    assert response == "\nFailed to process."
    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def testUserSSHExecutorNone(*_):
    _ = UserModel.objects.create(username='admin', user_type=UserType.ADMIN, uuid='uuid', password='pass',
                                 salt='salt', email='email@email.com', token='my_only_token',
                                 token_expire_time=round(time.time()) + 100)
    _ = TaskSettings.objects.create(name='test', uuid='my_uuid', description='', container_config='{}',
                                    time_limit=1, replica=1, ttl_interval=1, max_sharing_users=1)
    with mock.patch.object(wsocket.views, 'stream', mock_stream):
        communicator = WebsocketCommunicator(UserWebSSH,
                                             "/user_terminals/?uuid=my_uuid&token=my_only_token&username=admin")
        connected, _ = await communicator.connect()
        assert connected
        response = await communicator.receive_from()
        assert response == '\nExecutor is initializing, please wait.'
        await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def testUserSSHExecutorNormal(*_):
    _ = UserModel.objects.create(username='admin', user_type=UserType.ADMIN, uuid='uuid', password='pass',
                                 salt='salt', email='email@email.com', token='my_only_token',
                                 token_expire_time=round(time.time()) + 100)
    _ = TaskSettings.objects.create(name='test', uuid='my_uuid', description='', container_config='{}',
                                    time_limit=1, replica=1, ttl_interval=1, max_sharing_users=1)
    with mock.patch.object(wsocket.views, 'stream', mock_stream):
        TaskExecutor._instance = MockTaskExecutor()
        communicator = WebsocketCommunicator(UserWebSSH,
                                             "/user_terminals/?uuid=my_uuid&token=my_only_token&username=admin")
        connected, _ = await communicator.connect()
        assert connected
        response = await communicator.receive_from()
        assert response == 'Hello from WebSocket!\n'
        _ = await communicator.send_to('hello')
        await communicator.disconnect()