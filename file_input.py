fname = raw_input('Enter a file name')
try:
    fhand=open(fname)
except:
    print "File cannot be opened!",fname
    exit()
count=0
for line in fhand:
    if line.startswith('mylcd'):
        count = count + 1
        line = line.rstrip()
        print line
print "there were ", count, 'subject lines in ', fname