import os
import hashlib
import json
import time
import sys

directory = '/EXCITE/datasets/arxiv/pdfs'

def calc_hash(file):
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(file, 'rb') as f:
        buffer = f.read()
        sha256.update(buffer)
        md5.update(buffer)
        sha1.update(buffer)
    return {
        "sha256" : sha256.hexdigest(),
        "sha1": sha1.hexdigest(),
        "md5" : md5.hexdigest()
    }

cnt = 0
start = time.time()
if __name__ == '__main__':
    for root, dirs, files in os.walk(directory):
        for file in files:
            res = calc_hash(os.path.join(root, file))
            res['arxiv_id'] = file[:-4] # strip .pdf
            sys.stdout.write(json.dumps(res))
            sys.stdout.write("\n")
            cnt += 1
            if cnt % 100 == 0:
                sys.stderr.write(json.dumps({"elapsed" : time.time() - start, "processed" : cnt}))
                sys.stderr.write("\n")
                sys.stderr.flush()
                sys.stdout.flush()
    sys.stderr.flush()
    sys.stdout.flush()
