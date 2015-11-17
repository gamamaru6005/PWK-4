""" pwbib_parse0.py
    Nov. 16, 2015.  Test module to parse pwbib
    Command-line usage:
    python pwbib_parse0.py <pwbibx.txt>
"""
import codecs,sys,re

class Pwbib(object):
 """ a record corresponding to a relevant line of pwbibx.txt"""
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.n = n # line number in file
  self.line = line  # the unparsed line
  self.ok=False
  try:
   m = re.search(r'^([+.]+)(.*?) == (.*)\(vol[.] *([1-6])\) *$',line)
   if m:
    self.type='=='
    self.ok = True
    if m.group(1) == '+.':
     self.checked = True
    else:
     self.checked = False
    self.abbrv = m.group(2)
    self.title = m.group(3)
    self.volume = m.group(4)
   else:
    m = re.search(r'^([+.]+)([^ ]+) +(.*)\(vol[.] *([1-6])\) *$',line)
    if m:
     self.type='xx'
     self.ok = True
     if m.group(1) == '+.':
      self.checked = True
     else:
      self.checked = False
     self.abbrv = m.group(2)
     self.title = m.group(3)
     self.volume = m.group(4)
    else:
     print "ERROR parsing",n,line.encode('utf-8')
     exit(1)
  except:
   pass

def parse(filein):
 f = codecs.open(filein,"r","utf-8")
 recs = [] # return list of Pwbib records
 dbg = False # no debug messages for skipped lines
 n = 0
 for line in f:
  n = n + 1
  if not (line.startswith('+.') or line.startswith('.')):
   if dbg:
    print "skip line",n,line.encode('utf-8')
   continue
  rec = Pwbib(line,n)
  if not rec.ok:
   print "Format problem with line",n
   print line.encode('utf-8')
   continue
  recs.append(rec)
 f.close()
 return recs

if __name__ == "__main__":
 filein = sys.argv[1]
 recs = parse(filein)
 print len(recs),"parsed from",filein

