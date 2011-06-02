import os
import sys

if len(sys.argv) != 2:
  print 'Call with argument bulk or web!'
  exit(0)

arg = sys.argv[1]

print 'Processing ' + arg

if arg == 'bulk' or arg == 'web':
  pids = open('../getData/' + arg + '.pid','r')
  scripts = open('../getData/' + arg + '-pys','r')

p = pids.readlines()
s = scripts.readlines()

assert len(p) == len(s)

v = [0] * len(p)

while 0 in v:
  for i in range(len(p)):
    if v[i] == 0:
      # USE A CROSS PLATFORM METHOD!
      if os.path.exists('/proc/'+p[i][:-1]) == False:
        v[i] = 1
#        print "Find for:" + s[i][:-4]
        os.system('find ' + '../../data/' + s[i][:-4] + '-data -type f | sed "$d" | cut -d "/" -f 5- > ' + '../../data/' + s[i][:-4] + '-data/filelist')
#        os.system('cat ../../data/' + s[i][:-4] + '-data/filelist')
#        os.system('ls -alh ../../data/' + s[i][:-4] + '-data/')
        os.system('python ' + '../getTrec/' + s[i][:-1] + ' &')


os.remove('../getData/' + arg + '.pid')
os.remove('../getData/' + arg + '-pys')

print 'Finished calling the ' + arg + ' medical data to TREC conversion processes.'
