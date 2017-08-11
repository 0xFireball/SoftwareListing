
# SoftwareListing tool

import argparse
import json

def main():
    parser = argparse.ArgumentParser(description = "SoftwareListing tool")
    parser.add_argument("source", help="The source directory containing the configuration")
    parser.add_argument("dest", help="The output directory")
    args = parser.parse_args()
    
    # read metadata
    metafile = 'meta.json'
    with open(f'{args.source}/{metafile}') as meta_file:
        meta = json.load(meta_file)
    print(meta)

if __name__ == "__main__":
    main()
