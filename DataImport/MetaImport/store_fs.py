from __future__ import print_function
import json, os
from pathlib import Path
    
class store:
    def __init__(self, base_path):
        self.base = Path(base_path)
        assert(self.base.is_dir())
        assert(os.access(self.base.as_posix(), os.W_OK))
        
    def exists(self, key):
        return (self.base / key).exists()

    def set(self, key, value):
        file = self.base / key
        with file.open(mode='w') as fh:
            fh.write(json.dumps(value).decode('utf-8'))

    def get(self, key):
        file = self.base / key
        if not self.exists(key):
            return null
        with file.open(mode='r') as fh:
            return json.loads(fh.read())

    def delete(self, key):
        file = self.base / key
        if file.exists():
            file.unlink()
    
if __name__ == "__main__":
    # test the module
    s = store("./test-db")
    key = "test-redis-123"
    print(s.exists(key))
    print(s.set(key, [1,2,3]))
    print(s.get(key))
    print(s.exists(key))
    print(s.delete(key))
    print(s.exists(key))
