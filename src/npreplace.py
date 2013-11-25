#!/usr/bin/python

import argparse
import json
import pystache
import sys

def main():
    parser = argparse.ArgumentParser(description='Code Generator',
                                     epilog='Avoiding the boring part of the code...')

    parser.add_argument('-m', '-param_file', dest='param_file',
                            type=argparse.FileType('r'),
                            help='Path to the parameter file')

    parser.add_argument('source', metavar='FILE',
                            type=argparse.FileType('r'), default=sys.stdin,
                            help='file')

    print pystache.render(args.source.read(), args.param_file.read())

if __name__ == "__main__":
    main()
