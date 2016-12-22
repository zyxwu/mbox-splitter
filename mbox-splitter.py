# -*- coding: utf-8 -*-

import mailbox
import sys
from os.path import exists

if len(sys.argv) != 3:
    print
    print 'Usage: `python mbox-splitter.py filename.mbox size`'
    print '         where `size` is a positive integer in Mb'
    print
    print 'Example: `python mbox-splitter.py inbox_test.mbox 50`'
    print '         where inbox_test.mbox size is about 125 Mb'
    print
    print 'Result:'
    print 'Created file `inbox_test_1.mbox`, size=43Mb, messages=35'
    print 'Created file `inbox_test_2.mbox`, size=44Mb, messages=2'
    print 'Created file `inbox_test_3.mbox`, size=30Mb, messages=73'
    print 'Done'
    exit()


filename = sys.argv[1]
if not exists(filename):
    print 'File `{}` does not exist.'.format(filename)
    exit()

try:
    split_size = int(sys.argv[2])*1024*1024
except ValueError:
    print 'Size must be a positive number'
    exit()

if split_size < 1:
    print 'Size must be a positive number'
    exit()

if mailbox.mbox(filename).__len__() == 0:
    print 'Email messages in `{}` not found.'.format(filename)
    exit()


chunk_count = 1
output = filename.replace('.mbox', '_' + str(chunk_count) + '.mbox')
if exists(output):
    print 'The file `{}` has already been splitted. Delete chunks to continue.'.format(filename)
    exit()

print 'Splitting `{}` into chunks of {}Mb ...\n'.format(filename, sys.argv[2])
total_size = 0
of = mailbox.mbox(path=output, create=True)
mc = 0

for message in mailbox.mbox(filename):
    mc += 1
    message_size = str(message).__sizeof__()

    if total_size + message_size >= split_size:
        of.flush()
        of.close()
        chunk_count += 1
        print 'Created file `{}`, size={}Mb, messages={}.'.format(output, total_size/1024/1024, mc)
        total_size = 0
        output = filename.replace('.mbox', '_' + str(chunk_count) + '.mbox')
        of = mailbox.mbox(path=output, create=True)
        mc = 0

    of.add(message)
    total_size += message_size

print 'Created file `{}`, size={}Mb, messages={}.'.format(output, total_size/1024/1024, mc)
of.flush()
of.close()
print '\nDone'
