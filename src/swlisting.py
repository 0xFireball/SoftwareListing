
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
    meta_file = 'meta.json'
    with open(f'{args.source}/{meta_file}') as meta_file:
        meta = json.load(meta_file)

    item_source = f'{args.source}/items'
    if not os.path.exists(item_source):
        print(f'Error: Item directory {item_source} does not exist.')
        sys.exit(1)

    item_noun = meta["itemNoun"]
    
    item_output_dir = f'{args.dest}/{item_noun}'
    # create output dir
    for output_dir in [args.dest, item_output_dir]:
        if not os.path.exists(output_dir):
            print(f'Creating output directory {output_dir}')
            os.makedirs(output_dir)

    # load and generate pages
    item_paths = os.listdir(item_source)

    template_path = './template'
    template_items_path = f'{template_path}/{item_noun}'

    gen_item_listings = { }
    gen_items = []

    out_ext = tpl_ext = '.html'

    # load listing template
    listing_template_name = f'listing.{tpl_ext}'
    listing_template_path = f'{template_path}/{listing_template_name}'

    # generate item pages
    for item_path in item_paths:
        # parse page
        with open(f'{item_source}/{item_path}') as item_file:
            item_info = json.load(item_file)
        
        # load template
        tpl_path = f'{template_items_path}/{item_info["type"]}.{tpl_ext}'
        with open(tpl_path) as tpl_file:
            tpl_cont = tpl_file.read()

        st = StacheProcessor(tpl_cont)
        st.put('name', item_info['name'])

        res = st.read()
        # write to output file
        item_id = item_path.split(".")[0]
        output_file_path = f'{item_output_dir}/{item_id}.{out_ext}'
        with open(output_file_path, 'w') as output_file:
            output_file.write(res)
        print(f'Generated listing page for {item_id} in {output_file_path}')

        gen_items.append(item_id)
        gen_item_listings[item_id]

    # generate index page

if __name__ == "__main__":
    main()
