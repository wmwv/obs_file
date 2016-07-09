#!/usr/bin/env python

import argparse

import lsst.daf.persistence as dafPersist
import lsst.afw.display as afwDisplay


def do_display(repo, filename):
    display = afwDisplay.getDisplay()

    butler = dafPersist.Butler(repo)
    dataId = {'filename': filename}
    exp = butler.get('calexp', dataId=dataId)
    src = butler.get('src', dataId=dataId)

    with display.Buffering():
        display.mtv(exp)

        for s in src:
            if s['parent'] == 0:
                display.dot('o', s.getX(), s.getY(), ctype='blue')
            else:
                display.dot('+', s.getX(), s.getY(), ctype='red')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display an image with sources')
    parser.add_argument('repository', type=str, help='Path to output data repository')
    parser.add_argument('filename', type=str, help='Name of file that was processed')
    args = parser.parse_args()
    do_display(args.repository, args.filename)