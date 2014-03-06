#!/usr/bin/env python
import argparse
import sys

# Add your own breed!
dogs = {
# This is the default
'puppy': '''
     __
    (,'`-;  @@
    / ,-` 
   /  |
(\/_)_\_''',
# And because this meme just will not die, and people would add it anyway, I've
# added this in advance
'shiba': '''   ,    ,
  _|\__/ | 
 /     ` (
/ o,,o  \ \  @@
|,#*     )|
 >^-'   ' \ 
|`---      `'''
}

def bark(dog, message, quiet=False):
    template = dogs[dog].split('\n')
    message = message.split('\n')
    message = [line.replace('\t', '    ') for line in message]
    if quiet:
        rowLength = max([len(l) for l in message])
        rows = []
        rows.append('  ,{},'.format(''.join(['-'] * rowLength)))
        for line in message:
            rows.append(' |{{: ^{}}}|'.format(rowLength + 2).format(line))
        rows.append('_L-{}\''.format(''.join(['-'] * rowLength)))
    else:
        rowLength = max([len(l) // 2 for l in message])
        rows = []
        rows.append('  \\\'{}/'.format(''.join(['v\''] * rowLength)))
        for line in message:
            rows.append(' <{{: ^{}}}>'.format(rowLength * 2 + 3).format(line))
        rows.append('_=^,{}\\'.format(''.join(['^,'] * rowLength)))
    output = []
    start = -1
    # Reverse everything so that we construct the message from the bottom first
    template.reverse()
    for line in template:
        if start < 0:
            start = line.find('@@')
        if start >= 0 and rows:
            line = '{{: <{}}}'.format(start).format(line)
            line = line[:start] + rows.pop()
        output.append(line)
    rows.reverse()
    # If we have something left over after the message, put that on the top
    for line in rows:
        output.append('{{: >{}}}'.format(start + len(line)).format(line))
    output.reverse()
    return '\n'.join(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('message',
        help='the message',
        nargs='*',
        default='-')
    parser.add_argument('-b', '--breed',
        dest='breed',
        default='puppy',
        # Hidden until more breeds are added
        help=argparse.SUPPRESS)
    # Easter egg!
    parser.add_argument('-d', '--doge',
        dest='breed',
        action='store_const',
        const='shiba',
        help=argparse.SUPPRESS)
    parser.add_argument('-q', '--quiet',
        default=False,
        action='store_const',
        const=True,
        help='make output quieter')

    args = parser.parse_args()
    if args.message == ['-']:
        args.message = sys.stdin.read().rstrip('\n')
    else:
        args.message = ' '.join(args.message)
    print(bark(args.breed, args.message, args.quiet))
