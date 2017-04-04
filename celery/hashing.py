import os
import hashlib
import json
import time

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
    return {"sha256" : sha256.hexdigest(),
            "sha1": sha1.hexdigest(),
            "md5" : md5.hexdigest()
            }

if __name__ == '__main__':
    output = open('hashes.json', 'x')
    num_files = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            num_files += 1
    num_processed = 1
    hashes = []
    start = time.time()
    for root, dirs, files in os.walk(directory):
        for file in files:
            num_processed += 1
            res = calc_hash(os.path.join(root,file))
            res['arxiv_id'] = file.split('.')[0]
            hashes.append(res)
            if num_processed % 5000 == 0:
                print("Processing file {} out of {}. Percentage done: {}".format(num_processed, num_files,
                                                                                 num_processed / float(num_files)))
                print("Time elapsed {}".format(time.time() - start))
                for hash_obj in hashes:
                    json.dump(hash_obj, output)
                    output.write('\n')
                hashes = []
    output.close()

