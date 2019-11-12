

import argparse

from astop import *


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Search bag files recursively from designated directory.')

    # sub commands
    subparser = parser.add_subparsers()

    parser_meta = subparser.add_parser('meta', help='see `meta -h`')
    parser_meta.set_defaults(cmd_path='/subcmd_meta.py', preproc=PreprocCmdMeta)
    parser_meta.add_argument('-f',help='python boolean expression to filter bagfiles, default: True', type=str, default="True")
    parser_meta.add_argument('-p', help='target path, default: current directory', type=str, default="./")

    parser_data = subparser.add_parser('data', help='see `data -h`')
    parser_data.set_defaults(cmd_path='/subcmd_data.py', preproc=PreprocCmdData)
    parser_data.add_argument('topic', help='topic name', type=str)
    parser_data.add_argument('-f', help='python boolean expression to filter messages in each bagfile, default: True', type=str, default="True")
    parser_data.add_argument('-p', help='target path, default: current directory', type=str, default="./")    

    parser_info = subparser.add_parser('info', help='see `meta -h`')
    parser_info.set_defaults(cmd_path='/subcmd_info.py', preproc=PreprocCmdInfo)
    parser_info.add_argument('topic',help='topic name', type=str)
    parser_info.add_argument('-p', help='target path, default: current directory', type=str, default="./")    
    
    parser_mkindex = subparser.add_parser('mkindex', help='see `meta -h`')
    parser_mkindex.set_defaults(cmd_path='/subcmd_mkindex.py', preproc=PreprocCmdMkindex)
    parser_mkindex.add_argument('-p', help='target path, default: current directory', type=str, default="./")     

    parser_index = subparser.add_parser('index', help='see `data -h`')
    parser_index.set_defaults(cmd_path='/subcmd_index.py', preproc=PreprocCmdIndex)
    parser_index.add_argument('-f', help='python boolean expression to filter messages in each bagfile, default: True', type=str, default="True")



    # parse command line arguments
    args = parser.parse_args()


    aa = AstArgs(args)
    tf = args.preproc(aa)
    na = tf.visit(aa.src)

    code = compile(na,'<string>','exec')

    # run command
    exec(code)

