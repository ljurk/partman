from colorama import Fore, Style, init
import requests
import argparse
import json

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

def categories(args):
    r = requests.get(host + '/categories')

    r.status_code
    for data in r.json()['categories']:
        formatData(data,0)
        print('')


def show(args):
    r = requests.get(host + '/parts')

    r.status_code
    for data in r.json()['parts']:
        formatData(data,0)
        print('')

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
    show_parser.set_defaults(func=show)
    
    # process args for `show` command
    show_parser = subparsers.add_parser('categories', aliases=['cats'], help="show the contents of an entry")
    show_parser.set_defaults(func=categories)
    
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
