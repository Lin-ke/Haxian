
from typing import Any
from minio import Minio
class single:
    def __init__(self,cls) -> None:
        self.cls = cls
        self.cls.instance = None
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if not self.cls.instance:
            self.cls.instance = self.cls(*args, **kwds)
        return self.cls.instance
@single
class decorated_minio:
    def __init__(self) -> None:
        args = {
           "endpoint" : "localhost:9000",
	"access_key": "123",
	"secret_key": "12345678",
	"secure": False}
        self.client = Minio(**args)
   
client = decorated_minio().client
