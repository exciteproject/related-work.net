from __future__ import print_function
import json, os, io
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
        with io.open(str(file), mode='wb') as fh:
            fh.write(json.dumps(value, ensure_ascii=False).encode('utf8'))
        print("Saved to file: {}".format(file))

    def get(self, key):
        file = self.base / key
        if not self.exists(key):
            return None
        with io.open(str(file), mode='rb') as fh:
            return json.loads(fh.read().decode('utf8'))

    def delete(self, key):
        file = self.base / key
        if file.exists():
            file.unlink()

    def list(self):
        return (q.name for q in self.base.iterdir())
    
if __name__ == "__main__":
    # test the module
    s = store("./test-db")
    key = "test-redis-123"
    print(s.exists(key))
    print(s.set(key, [1,2,3, { 'unicode-example' : "☂" }]))
    print(s.get(key))
    print(s.exists(key))
    print(s.delete(key))
    print(s.exists(key))
