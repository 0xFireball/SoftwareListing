
# SoftwareListing tool

import argparse
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser(description = "SoftwareListing tool")
    parser.add_argument("source", help="The source directory containing the configuration")
    parser.add_argument("dest", help="The output directory")
    args = parser.parse_args()
    
    # read metadata
    metafile = 'meta.json'
    with open(f'{args.source}/{metafile}') as meta_file:
        meta = json.load(meta_file)

    itempath = f'{args.source}/items'
    if not os.path.exists(itempath):
        print(f'Error: Item directory {itempath} does not exist.')
        sys.exit(1)
    
    # create output dir
    if not os.path.exists(args.dest):
        print(f'Creating output directory {args.dest}')
        os.makedirs(args.dest)

    # load and generate pages
    itempaths = os.listdir(itempath)

    for itempath in itempaths:
        # parse page
        with open(itempath) as item_file:
            item_info = json.load(item_file)
        

if __name__ == "__main__":
    main()
