# mailxfer
Tools for migrating IMAP mailboxes between hosts

## Problem
Migrating from self-hosted email to a provider left me with a large amount of mail to move between hosts, and the tools provided worked mainly with known vendors and migrated an entire mailbox. I needed something to specify individual folders to shift, and possibly to a different folder name on the destination.

## Solution
**mailxfer.py** - specify the IMAP hosts, the usernames for each, and the to/from folder in the script. The passwords are supplied when it runs.

**getmessage.py** - pull a single message. Specify the IMAP server and username in the script. Supply the folder name and the number of the email on the command line. *NOTE: This is the number of the message in the folder, not the Message-ID.*

**dedupe.py** - spin through all messages in a folder and count the number that have a Message-ID that has already been seen. Optionally delete the duplicates. Provide the host and username in the script, password when it runs.

## Known Issues
The script does not deal well with malformed emails. Message-ID's that are not in the correct format will likely cause it to bomb and I was not all that interested in fixing that elegantly rather than just deleting the offending email and continuing.
If you are transferring a large amount of spam emails you will likely run into this enough to be annoying. In particular, there is one particular spammer/spam script that generates random sender/subject emails with just an image in the body, that tends to create emails that just wont be accepted by some of the major mailbox providers.

## Warranty
NONE! Use it at your own risk. If this helps you, good. If it doesnt, then you own both pieces.
