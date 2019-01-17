from colorama import Fore, Style, init
import requests
import argparse
import json
import csv

host = 'http://localhost:5001'
#colors
cRed = Style.BRIGHT + Fore.RED
cDefault = Style.RESET_ALL
cGreen = Style.BRIGHT + Fore.GREEN
cYellow = Style.BRIGHT + Fore.YELLOW

#show recursive
def formatData(t,s):
    if not isinstance(t,dict) and not isinstance(t,list):
        print(cGreen+":"+str(t) ,end='')
    else:
        for key in t:
            print(cDefault + '\n' + "> "*s+str(key), end='')
            if not isinstance(t,list):
                formatData(t[key],s+1)

def show(args):
    r = requests.get(host + '/' + args.path)
    r.status_code
    for data in r.json()[args.path]:
        formatData(data,0)
        print('')

def add(args):
    if args.path == 'category':
        if args.name != None:
            r = requests.put(host + '/categories', data = {'name':args.name})
            print(r.text)
        elif args.csv != None:
            list = []
            with open(args.csv,'r') as f:
                rows = csv.DictReader(f, delimiter=';')
                for row in rows:
                    list.append(row)
            for l in list:
                r = requests.put(host + '/categories', data = {'name':l['name']})
                print(r.text)
    elif args.path == 'part':
        if args.name != None and args.categoryId != None and args.description != None:
            r = requests.put(host + '/parts', data = {'name':args.name, 'categoryId': args.categoryId, 'description': args.description})
        elif args.csv != None:
            list = []
            with open(args.csv,'r') as f:
                rows = csv.DictReader(f, delimiter=';')
                for row in rows:
                    list.append(row)
            for l in list:
                r = requests.put(host + '/parts', data = {'name':l['name'], 'categoryId': l['categoryId'], 'description': l['description'], 'amount': l['amount']})
                print(r.text)

def export(args):
    r = requests.get(host + '/' + args.path)
    toCsv = r.json()
    toCsv = toCsv[args.path]
    keys = toCsv[0].keys()
    with open(args.file, 'w') as f:
        f = csv.DictWriter(f, keys, delimiter=';')
        f.writeheader()
        for row in toCsv:
            f.writerow(row)

def createParser():
    """Create argparse object"""

    parser = argparse.ArgumentParser(description="Append -h to any command to view its syntax.")
    parser._positionals.title = "commands"

    subparsers = parser.add_subparsers()
    subparsers.dest = 'command'
    subparsers.required = True

    path_help = "entry path (e.g. 'foo') or group path (e.g. 'foo/')"

    # process args for `show` command
    show_parser = subparsers.add_parser('show', help="show the contents of an entry")
    show_parser.add_argument('path', metavar='PATH', type=str, help='value to add')
    show_parser.set_defaults(func=show)

    # process args for `add` command
    addParser = subparsers.add_parser('add', help="show the contents of an entry")
    addParser.add_argument('path', metavar='PATH', type=str, help='value to add')
    addParser.add_argument('--name', metavar='NAME', type=str, default=None, help="name of part")
    addParser.add_argument('--categoryId', metavar='CATEGORYID', type=int, default=None, help="id of category")
    addParser.add_argument('--description', metavar='DESCRIPTION', type=str, default=None, help="description")
    addParser.add_argument('--csv', metavar='CSV', type=str, default=None, help="description")
    addParser.set_defaults(func=add)

    # process args for `export` command
    exportParser = subparsers.add_parser('export', help="show the contents of an entry")
    exportParser.add_argument('path', metavar='PATH', type=str, help='value to add')
    exportParser.add_argument('file', metavar='FILE', type=str, help='outputfile')
    exportParser.set_defaults(func=export)

    # optional arguments
    parser.add_argument('--debug', action='store_true', default=False, help="enable debug messages")

    return parser

def main():

    parser = createParser()
    args = parser.parse_args()

    if args.debug:
        print('Debugging enabled...')
        log.setLevel(logging.DEBUG)

    args.func(args)

if __name__ == '__main__':
    main()
