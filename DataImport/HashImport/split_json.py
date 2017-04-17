lines_per_file = 10000
smallfile = None
with open('/EXCITE/datasets/arxiv/hashes.json') as hashes:
    for line_num, line in enumerate(hashes):
        if line_num % lines_per_file == 0:
            if smallfile:
                smallfile.close()
            small_filename = 'arxiv_pdf_hashes_{:03.0f}.json'.format(line_num / lines_per_file)
            smallfile = open('/EXCITE/datasets/arxiv/hashes/' + small_filename, "w")
        smallfile.write(line)
    if smallfile:
        smallfile.close()