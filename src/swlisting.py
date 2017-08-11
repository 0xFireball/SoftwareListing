
# SoftwareListing tool

import argparse
import json
import os
import sys
from distutils.dir_util import copy_tree

from flatten_json import flatten
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

    item_noun = meta["itemNoun"]

    item_source = f'{args.source}/{item_noun}'
    if not os.path.exists(item_source):
        print(f'Error: Item directory {item_source} does not exist.')
        sys.exit(1)

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
    item_info_template_name = f'info.{tpl_ext}'
    item_info_template_path = f'{template_path}/{item_info_template_name}'
    with open(item_info_template_path) as item_info_template_file:
        item_info_template = item_info_template_file.read()

    # generate item pages
    for item_path in item_paths:
        item_id = item_path.split(".")[0]

        # parse page
        with open(f'{item_source}/{item_path}') as item_file:
            item_info = json.load(item_file)
    
        # flatten info as props
        item_props = flatten(item_info, '.')

        # load template
        page_tpl_path = f'{template_items_path}/page.{tpl_ext}'
        with open(page_tpl_path) as page_tpl_file:
            page_tpl = page_tpl_file.read()

        tpl_path = f'{template_items_path}/{item_info["type"]}.{tpl_ext}'
        with open(tpl_path) as tpl_file:
            tpl_cont = tpl_file.read()

        st = StacheProcessor(page_tpl)
        st.put('page', tpl_cont)
        tpl_cont = st.read()

        tpl_gen = []
        for template in [tpl_cont, item_info_template]:
            st = StacheProcessor(template)

            st.put('noun', item_noun)
            st.put('id', item_id)

            # add properties
            for key in item_props.keys():
                if isinstance(item_props[key], str):
                    st.put(key, item_props[key])

            res = st.read()
            tpl_gen.append(res)

        # write to output file
        output_file_path = f'{item_output_dir}/{item_id}.{out_ext}'
        with open(output_file_path, 'w') as output_file:
            output_file.write(tpl_gen[0]) # write out item listing page
        print(f'Generated listing page for {item_id} in {output_file_path}')

        gen_item_listings[item_id] = tpl_gen[1] # save short listing

    # generate listing and landing pages
    itemlist_template_name = f'listing.{tpl_ext}'
    itemlist_listing_path = f'{template_path}/{itemlist_template_name}'
    with open(itemlist_listing_path) as itemlist_tpl_file:
        itemlist_tpl = itemlist_tpl_file.read()

    landing_template_name = f'index.{tpl_ext}'
    landing_template_path = f'{template_path}/{landing_template_name}'
    with open(landing_template_path) as landing_tpl_file:
        landing_tpl = landing_tpl_file.read()

    st = StacheProcessor(itemlist_tpl)
    item_list_tpl = ''
    for item_id, item_listing in gen_item_listings.items():
        item_list_tpl += item_listing + '\n'
    st.put('listing', item_list_tpl)
    itemlist_tpl = st.read()

    tpls = []
    for tpl in [itemlist_tpl, landing_tpl]:
        st = StacheProcessor(tpl)
        # custom props
        for key in meta["props"].keys():
            st.put(key, meta["props"][key])

        # default props
        st.put('title', meta['title'])
        tpls.append(st.read())

    itemlist_tpl = tpls[0]
    landing_tpl = tpls[1]

    # write out listing page
    itemlist_output_path = f'{args.dest}/listing.{tpl_ext}'
    with open(itemlist_output_path, 'w') as itemlist_ouf:
        itemlist_ouf.write(itemlist_tpl)
    print(f'Wrote listing page to {itemlist_output_path}')

    # write out landing page
    landing_output_path = f'{args.dest}/index.{tpl_ext}'
    with open(landing_output_path, 'w') as landing_ouf:
        landing_ouf.write(landing_tpl)
    print(f'Wrote landing page to {landing_output_path}')

    # copy assets
    assets_dir_name = 'assets'
    assets_src_dir = f'{template_path}/{assets_dir_name}'
    assets_dest_dir = f'{args.dest}/{assets_dir_name}'
    print(f'Copying {assets_src_dir} to {assets_dest_dir}')
    copy_tree(assets_src_dir, assets_dest_dir)

if __name__ == "__main__":
    main()
