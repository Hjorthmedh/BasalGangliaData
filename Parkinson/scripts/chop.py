#!/usr/bin/python3
"""
Delete terminal dendritic segments in morphology.
"""

import sys
import argparse
from treem import Morph

def parse():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=str, help="input morphology (swc)")
    parser.add_argument("-o", dest="output", type=str, default='out.swc',
        help="output morphology (swc) [out.swc]")
    return parser.parse_args()


def main():
    args = parse()
    try:
        m = Morph(args.file)
        for node in m.root.leaves():
            dead = node.is_root() or node.type() == 1
            if not dead or node.type() == 3:
                m.prune(node)
        if not dead:
            m.save(args.output)
        else:
            print(f'{args.file} is dead')
    except:
        dead = True
        print(f'{args.file} is dead')
    return 0 if not dead else 1


if __name__ == "__main__":
    sys.exit(main())
