import argparse
import sys, os
import pathlib

import ocrconvert

parser = argparse.ArgumentParser(description="Recognize written text in images with Google OCR")
parser.add_argument("key", help="The API Key")
parser.add_argument("input", help="The input image file")
parser.add_argument("-o", "--output", help="The output file where text will be saved", default=None)
parser.add_argument("-r", "--recursive", help="Use this if input file is a directory", action="store_true")

def ocrconvert_file(inputf, outputf, keyf):
    with open(inputf, "rb") as infp, open(keyf, "r") as keyfp:
        if outputf == None:
            ocrconvert.full_annotate_text(keyfp.read(), infp)
            sys.exit(0)
        with open(outputf, "w") as outfp:
            ocrconvert.full_annotate_text(keyfp.read(), infp, outfp)

def ocrconvert_multifiles(inputf, outputf, keyf):
    with open(keyf, "r") as keyfp:
        ocrconvert.schedule_threads(keyfp.read(), inputf, outputf)

args = parser.parse_args()

SUPPORTED = [".jpg", ".png"]

if args.recursive == False and os.path.isdir(args.input) == False:
    ocrconvert_file(args.input, args.output, args.key)
elif args.recursive == False:
    print("Error: Input file is a directory. Use -r or --recursive option")
    sys.exit(0)
elif args.recursive == True and os.path.isdir(args.input) == True:
    outRoot = args.output
    inputf = []
    outputf = []
    if outRoot == None: 
        outRoot = "./output"
    for dirName, subDirList, fileList in os.walk(args.input):
        for fileName in fileList:
            # Check whether file is supported or not
            ext = fileName[fileName.rfind("."):]
            if ext not in SUPPORTED:
                continue
            # Create output directory if it doesn't exist
            outPath = os.path.join(outRoot, os.path.relpath(dirName, args.input))
            if os.path.exists(outPath) == False:
                pathlib.Path(outPath).mkdir(parents=True, exist_ok=True)
            inputf.append(os.path.join(dirName, fileName))
            outputf.append("{}/{}.txt".format(outPath, fileName[0:fileName.rfind(".")]))
    ocrconvert_multifiles(inputf, outputf, args.key)
