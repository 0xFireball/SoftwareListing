
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

    out_ext = tpl_ext = 'html'

    # load listing template
    listing_template_name = f'listing.{tpl_ext}'
    listing_template_path = f'{template_path}/{listing_template_name}'
    with open(listing_template_path) as listing_template_file:
        listing_template = listing_template_file.read()

    # generate item pages
    for item_path in item_paths:
        # parse page
        with open(f'{item_source}/{item_path}') as item_file:
            item_info = json.load(item_file)
        
        # load template
        tpl_path = f'{template_items_path}/{item_info["type"]}.{tpl_ext}'
        with open(tpl_path) as tpl_file:
            tpl_cont = tpl_file.read()

        tpl_gen = []
        for template in [tpl_cont, listing_template]:
            st = StacheProcessor(template)
            st.put('name', item_info['name'])

            res = st.read()
            tpl_gen.append(res)

        # write to output file
        item_id = item_path.split(".")[0]
        output_file_path = f'{item_output_dir}/{item_id}.{out_ext}'
        with open(output_file_path, 'w') as output_file:
            output_file.write(tpl_gen[0]) # write out item listing page
        print(f'Generated listing page for {item_id} in {output_file_path}')

        gen_item_listings[item_id] = tpl_gen[1] # save short listing

    # generate index page
    index_template_name = f'index.{tpl_ext}'
    index_listing_path = f'{template_path}/{index_template_name}'
    with open(index_listing_path) as index_tpl_file:
        index_tpl = index_tpl_file.read()

    st = StacheProcessor(index_tpl)
    item_list_tpl = ''
    for item_id, item_listing in gen_item_listings.items():
        item_list_tpl += item_listing + '\n'
    st.put('listing', item_list_tpl)
    # write out index page
    index_output_path = f'{args.dest}/index.{tpl_ext}'
    with open(index_output_path, 'w') as index_ouf:
        index_ouf.write(st.read())

if __name__ == "__main__":
    main()
