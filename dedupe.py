#!/usr/bin/env python

import re
import sys
import imaplib
import getpass

IMAP_SERVER = '<imap.server.com>'
EMAIL_ACCOUNT = "<username>"

delete = False
MSGIDS = []

def main():
    if len(sys.argv) < 2:
      print "Usage: dedupe.py <folder>\n"
      sys.exit()

    folder = sys.argv[1]
    dupes = 0

    if delete:
      print '\n** DELETION ENABLED **'

    print "\nIMAP password for %s on %s:" % (EMAIL_ACCOUNT, IMAP_SERVER)
    PASSWORD = getpass.getpass()

    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, PASSWORD)

    type, data = M.select(folder)
    if type != 'OK':
        print 'ERROR selecting mail folder'
        sys.exit()
    print '\nTotal Emails: %s (%s)' % (data[0], folder)

    type, data = M.search(None, "ALL")
    for num in data[0].split():

        print("\r"),
        print(num),

        type, msgdata = M.fetch(num, '(BODY.PEEK[HEADER])')
        if type != 'OK':
            print "ERROR getting message", num
            return
        found = re.search('[Mm]essage-[iI][dD]: ?<(.+?)>', str(msgdata[0]))
        if found:
            if found.group(1) in MSGIDS:
                dupes += 1
                if delete:
                    type, _ = M.store(num, '+FLAGS', '\\Deleted')
                    if type != 'OK':
                        print "ERROR deleting message", num
            else:
                MSGIDS.append(found.group(1))

    print '\nDuplicates  : %d\n' % (dupes)

if __name__ == "__main__":
  main()
