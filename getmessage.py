#!/usr/bin/env python

import sys
import imaplib
import getpass

IMAP_SERVER = 'red.keystealth.org'
EMAIL_ACCOUNT = "scott"

def main():
  if len(sys.argv) < 3:
    print "Usage: getmessage.py <folder> <message number>\n"
    sys.exit()

  folder = sys.argv[1]
  num = sys.argv[2]

  print "IMAP password for %s on %s:" % (EMAIL_ACCOUNT, IMAP_SERVER)
  PASSWORD = getpass.getpass()

  M = imaplib.IMAP4_SSL(IMAP_SERVER)
  M.login(EMAIL_ACCOUNT, PASSWORD)

  type, data = M.select(folder)
  if type != 'OK':
    print 'ERROR selecting mail folder'
    sys.exit()

  flags = M.fetch(num, '(FLAGS)')[1]
  print(flags)

  type, data = M.fetch(num, '(BODY.PEEK[])')
  if type != 'OK':
    print "ERROR getting message", num
    sys.exit()

  print data

if __name__ == "__main__":
  main()
