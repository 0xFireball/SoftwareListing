
# SoftwareListing tool

import argparse
import json
import os
import sys

from stache import StacheProcessor

def main():
    parser = argparse.ArgumentParser(description = "SoftwareListing tool")
    parser.add_argument("source", help="The source directory containing the configuration")
    parser.add_argument("dest", help="The output directory")
    args = parser.parse_args()
    
    # read metadata
    metafile = 'meta.json'
    with open(f'{args.source}/{metafile}') as meta_file:
        meta = json.load(meta_file)

    item_source = f'{args.source}/items'
    if not os.path.exists(item_source):
        print(f'Error: Item directory {item_source} does not exist.')
        sys.exit(1)
    
    # create output dir
    if not os.path.exists(args.dest):
        print(f'Creating output directory {args.dest}')
        os.makedirs(args.dest)

    # load and generate pages
    itempaths = os.listdir(item_source)

    template_path = './template'
    template_items_path = f'{template_path}/items'

    for itempath in itempaths:
        # parse page
        with open(f'{item_source}/{itempath}') as item_file:
            item_info = json.load(item_file)
        
        # load template
        tpl_path = f'{template_items_path}/{item_info["type"]}.html'
        with open(tpl_path) as tpl_file:
            tpl_cont = tpl_file.read()

        st = StacheProcessor(tpl_cont)
        st.put('name', item_info['name'])

        res = st.read()
        print(res)

if __name__ == "__main__":
    main()
