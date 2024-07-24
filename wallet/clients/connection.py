import threading
import time


class Connection:
    def __init__(self, rpc_url, timeout=10, cache_size=100):
        self.rpc_url = rpc_url
        self.timeout = timeout
        self.cache_size = cache_size
        self._lock = threading.Lock()
        self._connection = None
        self._last_used = None

    def connect(self):
        """
        Establish a new RPC connection or reuse an existing one if it's still valid.
        """
        with self._lock:
            if self._connection is None or self._is_connection_expired():
                self._connection = self._create_connection()
                self._last_used = time.time()
            return self._connection

    def _create_connection(self):
        """
        Create a new RPC connection. This should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def _is_connection_expired(self):
        """
        Check if the connection has expired based on the timeout.
        """
        if self._last_used is None:
            return True
        return (time.time() - self._last_used) > self.timeout

    def close(self):
        """
        Close the RPC connection and clean up resources.
        """
        with self._lock:
            if self._connection is not None:
                self._connection = None
                self._last_used = None
