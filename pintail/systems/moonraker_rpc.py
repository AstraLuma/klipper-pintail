import concurrent.futures
import dataclasses
import itertools
import json
import socket
import threading
import typing
import queue


class RPCError(Exception):
    """
    Raised when the remote server raises an error
    """
    code: int
    message: str
    data: typing.Any

    def __init__(self, code, message, data):
        super().__init__(code, message, data)
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        return f"{self.code}: {self.message}"


@dataclasses.dataclass
class Event:
    """
    https://moonraker.readthedocs.io/en/latest/web_api/#websocket-notifications
    """
    name: str
    params: list


class MoonrakerUDS:
    """
    Talk to moonraker over JSON-RPC via Unix Domain Socket
    """
    _socket: socket.socket
    _future_results: dict[int, concurrent.futures.Future]
    events: queue.SimpleQueue

    def __init__(self, path):
        self._id_generator = itertools.count()
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._socket.connect(path)
        self._future_results = dict()
        self.events = queue.SimpleQueue()
        self._thread = threading.Thread(None, self._read_thread, name=f"moonraker-reader:{path}", daemon=True)
        self._thread.start()

    def close(self):
        self._socket.close()
        self._thread = None
        # Hopefully the read thread kills itself

    _delimiter = b"\x03"

    def _send(self, req):
        self._socket.sendall(json.dumps(req).encode('utf-8') + self._delimiter)

    _bufsize = 4096
    _readbuf = b""

    def _read_one(self):
        while self._delimiter not in self._readbuf:
            self._readbuf += self._socket.recv(self._bufsize)
        
        packet, _, self._readbuf = self._readbuf.partition(self._delimiter)

        return json.loads(packet.decode('utf-8'))

    def _read_thread(self):
        while True:
            try:
                msg = self._read_one()
            except OSError:
                return
            # print(f"{msg=}", flush=True)
            if "id" in msg:
                # Response to a request
                self._future_results[msg["id"]].set_result(msg)
            else:
                # Broadcast event
                self.events.put(Event(msg["method"], msg.get("params", [])))

    def __call__(self, method: str, /, *pargs, **kwargs):
        """
        Make one JSON-RPC request and get one response.
        """
        assert not (pargs and kwargs)
        reqid = next(self._id_generator)
        req = {
            "jsonrpc": "2.0",
            "method": method,
            "id": reqid,
        }
        if pargs:
            req['params'] = pargs
        elif kwargs:
            req['params'] = kwargs
        else:
            pass

        self._future_results[reqid] = fut = concurrent.futures.Future()
        self._send(req)
        resp = fut.result()

        assert resp['id'] == reqid

        if 'result' in resp:
            return resp['result']
        elif 'error' in resp:
            e = resp['error']
            raise RPCError(e['code'], e['message'], e.get('data', None))
        else:
            raise RuntimeError("JSON-RPC response neither result nor error")

