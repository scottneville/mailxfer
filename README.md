# mailxfer
Tools for migrating IMAP mailboxes between hosts

## Problem
Migrating from self-hosted email to a provider left me with a large amount of mail to move between hosts, and the tools provided worked mainly with known vendors and migrated an entire mailbox. I needed something to specify individual folders to shift, and possibly to a different folder name on the destination.

## Solution
mailxfer.py - specify the IMAP hosts, the usernames for each, and the to/from folder in the script. The passwords are supplied when it runs.
getmessage.py - pull a single message. Specify the IMAP server and username in the script. Supply the folder name and the number of the email on the command line. *NOTE: This is the number of the message in the folder, not the Message-ID.

## Warranty
NONE! Use it at your own risk. If this helps you, good. If it doesnt, then you own both pieces.
