#!/usr/bin/env python

import re
import sys
import time
import imaplib
import getpass
import datetime
from time import struct_time
from dateutil import parser

S_IMAP_SERVER = '<source.server.com>'
D_IMAP_SERVER = '<destination.server.com>'

S_EMAIL_ACCOUNT = "<source username>"
D_EMAIL_ACCOUNT = "<destination username>"

S_EMAIL_FOLDER = "Inbox"
D_EMAIL_FOLDER = "Inbox"

D_MSGID=[]

print "\nSource password:"
S_PASSWORD = getpass.getpass()
print "Destination password:"
D_PASSWORD = getpass.getpass()

print

S = imaplib.IMAP4_SSL(S_IMAP_SERVER)
D = imaplib.IMAP4_SSL(D_IMAP_SERVER)


def move_msg(num):
    flags = S.fetch(num, '(FLAGS)')[1][0]
    found = re.search('FLAGS \((.*?)\)', flags)
    flags = found.group(1)
    if not flags:
        flags = None

    rv, data = S.fetch(num, '(BODY.PEEK[])')

    date = S.fetch(num, '(INTERNALDATE)')[1][0].split("\"")[1]
    date = parser.parse(date)
    date = date.timetuple()

    rv, _ = D.append(D_EMAIL_FOLDER, flags, date, data[0][1])
    if rv != 'OK':
        print "ERROR getting message", num
        return False

    rv, _ = S.store(num, '+FLAGS', '\\Deleted')
    if rv != 'OK':
        print "ERROR deleting message", num
        return False

    # Add delay to avoid the destination server rate limiting my connection.
    time.sleep(1)

    return True

def found_on_dest(msgid):
    global D

    try:
        rv, msgnums = D.search(None, 'HEADER', 'Message-ID', msgid)
    except:
        print "ERROR searching for [%s] on %s" % (msgid, D_IMAP_SERVER)
        D.logout()
        D = imaplib.IMAP4_SSL(D_IMAP_SERVER)
        D.login(D_EMAIL_ACCOUNT, D_PASSWORD)
        D.select(D_EMAIL_FOLDER)
        rv, msgnums = D.search(None, 'HEADER', 'Message-ID', msgid)

    if msgnums[0]:
        return True

    return False

def main():
    DELETED = 0
    EXISTS = 0
    MOVED = 0
    FAILED = 0

    S.login(S_EMAIL_ACCOUNT, S_PASSWORD)
    D.login(D_EMAIL_ACCOUNT, D_PASSWORD)

    rv, data = S.select(S_EMAIL_FOLDER)
    print 'Source Emails: %s (%s)' % (data[0], S_EMAIL_FOLDER)

    rv, data = D.select(D_EMAIL_FOLDER)
    print 'Destination:   %s (%s)' % (data[0], D_EMAIL_FOLDER)
    print

    # Loop through all of the source emails:
    #   - if deleted, skip
    #   - if not deleted, check if msgid is in the dest list, if so skip/delete
    #   - if neither, copy to dest folder

    print "Looping through source message folder..."
    print

    rv, data = S.search(None, "ALL")
    for num in data[0].split():
        rv, msgdata = S.fetch(num, '(BODY.PEEK[HEADER])')
        if rv != 'OK':
            print "ERROR getting message", num
            return
        found = re.search('[Mm]essage-[iI][dD]: ?<(.+?)>', str(msgdata[0]))
        if found:
            MSGID = found.group(1)

            rv, msgdata = S.fetch(num, '(FLAGS)')
            if rv != 'OK':
                print "ERROR getting message", num
                return
            found = re.search('FLAGS.*Deleted.*\)', str(msgdata[0]))
            if found:
                DELETED += 1
                print '[%s] Deleted\t%s' % (num, MSGID)
            elif found_on_dest(MSGID):
                EXISTS += 1
                rv, _ = S.store(num, '+FLAGS', '\\Deleted')
                if rv != 'OK':
                    print "ERROR deleting message", num
                print '[%s] Exists\t%s' % (num, MSGID)
            else:
                if move_msg(num):
                    MOVED += 1
                    print '[%s] Moved\t%s' % (num, MSGID)
                else:
                    FAILED += 1
                    print '[%s] Failed\t%s' % (num, MSGID)
        else:
            FAILED += 1 

    print '\nDeleted:\t%d' % (DELETED)
    print 'Exists:\t\t%d' % (EXISTS)
    print 'Moved:\t\t%d' % (MOVED)
    print 'Failed:\t\t%d\n' % (FAILED)    

    S.logout()
    D.logout()

if __name__ == "__main__":
    main()
