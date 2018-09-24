"""Unit tests for send function in module bluserver.tools ."""

import pytest

from bluserver.tools import (
    send,
)


@pytest.fixture(scope='function')
def socket(mocker):
    """Factory fixture for generating sockets objects."""
    def inner_socket(send=False, recv=False):
        """Return a socket mocked object.

        Args:
            send (tuple): side_effect for send method
            recv (tuple): side_effect for recv method

        Returns:
            mocked socket object

        """
        mock_socket = mocker.MagicMock()
        if send:
            mock_socket.send.side_effect = send
        if recv:
            mock_socket.recv.side_effect = recv
        return mock_socket

    return inner_socket


def test_send_total(socket):
    """Data is sent in a single invocation of socket.send."""
    s = socket(send=(8,))
    send(s, b'12345678')

    assert s.send.call_count == 1

    args, kwargs = s.send.call_args
    assert not kwargs
    assert len(args) == 1
    assert args[0] == b'12345678'


def test_send_partial(socket):
    """Data is sent in multiples invocations of socket.send."""
    s = socket(send=(2, 2, 3, 1))
    send(s, b'12345678')

    assert s.send.call_count == 4

    args, kwargs = s.send.call_args_list[0]
    assert not kwargs
    assert len(args) == 1
    assert args[0] == b'12345678'

    args, kwargs = s.send.call_args_list[1]
    assert not kwargs
    assert len(args) == 1
    assert args[0] == b'345678'

    args, kwargs = s.send.call_args_list[2]
    assert not kwargs
    assert len(args) == 1
    assert args[0] == b'5678'

    args, kwargs = s.send.call_args_list[3]
    assert not kwargs
    assert len(args) == 1
    assert args[0] == b'8'


def test_send_error(socket):
    """Only the first 2 bytes could be sent because the connection was closed."""

    s = socket(send=(2, 0))

    with pytest.raises(RuntimeError) as excinfo:
        send(s, b'12345678')

    assert 'Socket connection is broken' in str(excinfo.value)

    assert s.send.call_count == 2

    args, kwargs = s.send.call_args_list[0]
    assert not kwargs
    assert len(args) == 1
    assert args[0] == b'12345678'

    args, kwargs = s.send.call_args_list[1]
    assert not kwargs
    assert len(args) == 1
    assert args[0] == b'345678'
