#!/usr/bin/python

from avro.io import DatumReader, DatumWriter
from avro.datafile import DataFileReader, DataFileWriter
from generator.mapreduce import JavaHadoopEntityGenerator, JavaHadoopComparatorGenerator, JavaHadoopParser

#, JavaHadoopComparatorGenerator, JavaHadoopParser, JavaHadoopPartitionerGenerator
import argparse
import avro.schema
import sys
import os

try:
    import json
except ImportError:
    import simplejson as json

def main():
    args = options_argparse()
    schema = avro.schema.parse(args.schema.read())

    #######################################################
    #  __  __      _      
    # |  \/  |__ _(_)_ _  
    # | |\/| / _` | | ' \ 
    # |_|  |_\__,_|_|_||_|
    #
    for generator in args.generators:
        code = generator.code_generator(schema)

        if args.src:
            path = os.path.join(args.src, generator.make_file_name(schema))
            parent = os.path.dirname(path)

            if not os.path.isdir(parent):
                os.makedirs(parent)

            with open(path, 'w') as writer:
                writer.write(code)

        else:
            print code

        #

def options_argparse():
    class AppendGenerator(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not hasattr(namespace, 'generators'):
                setattr(namespace, 'generators', [])

            namespace.generators.append(self.default)

    #
    parser = argparse.ArgumentParser(description='Code Generator',
                                     epilog='Avoiding the boring part of the code...')

    subparsers = parser.add_subparsers(title='Languages', help='Code generators')

    #######################################################
    #  __  __           ___        _             
    # |  \/  |__ _ _ __| _ \___ __| |_  _ __ ___ 
    # | |\/| / _` | '_ \   / -_) _` | || / _/ -_)
    # |_|  |_\__,_| .__/_|_\___\__,_|\_,_\__\___|
    #             |_|                            
    #parser_mapreduce_parent = subparsers.add_parser('mapreduce', help='MapReduce')
    parser_mapreduce = subparsers.add_parser('mapreduce', help='MapReduce')
    parser_mapreduce.add_argument('--entity', action=AppendGenerator, default=JavaHadoopEntityGenerator(),
                            nargs=0, help='Code generators')
    parser_mapreduce.add_argument('--group', action=AppendGenerator, default=JavaHadoopComparatorGenerator(JavaHadoopComparatorGenerator.GROUPING),
                            nargs=0, help='Code generators')
    parser_mapreduce.add_argument('--order', action=AppendGenerator, default=JavaHadoopComparatorGenerator(JavaHadoopComparatorGenerator.ORDER),
                            nargs=0, help='Code generators')
    parser_mapreduce.add_argument('--parser', action=AppendGenerator, default=JavaHadoopParser(),
                            nargs=0, help='Code generators')
    parser_mapreduce.add_argument('-s', '--src', metavar='SRC_FOLDER', dest='src',
                            help='Folder')
    parser_mapreduce.add_argument('schema', metavar='SCHEMA',
                            type=argparse.FileType('r'), default=sys.stdin,
                            help='avro file')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
