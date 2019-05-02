outfilename = 'korean_dic02.txt'
infilename = 'korean_dic01.txt'

#lines_seen = set() # holds lines already seen
outfile = open(outfilename, "w")
for line in open(infilename, "r"):
    elements = line.split('-')
    for element in elements:
        result = ''.join(element)
        outfile.write(result)
outfile.close()
