from __future__ import print_function
import redis
import json

class store:
    def __init__(self, **kwargs):
        self.r = redis.StrictRedis(**kwargs)

    def exists(self, key):
        return self.r.exists(key)

    def set(self, key, value):
        # nx=True Don't overwrite the key
        return self.r.set(key, json.dumps(value), nx=True)

    def get(self, key):
        raw = self.r.get(key)
        if not raw: return null
        return json.loads(raw)

    def delete(self, key):
        self.r.delete(key)
    
if __name__ == "__main__":
    # test the module
    s = store(db=3)
    key = "test-redis-123"
    print(s.exists(key))
    print(s.set(key, [1,2,3]))
    print(s.get(key))
    print(s.exists(key))
    print(s.delete(key))
    print(s.exists(key))
