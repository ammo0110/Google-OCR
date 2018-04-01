import argparse

import ocrconvert

parser = argparse.ArgumentParser(description="Recognize written text in images with Google OCR")
parser.add_argument("key", help="The API Key")
parser.add_argument("input", help="The input image file")
parser.add_argument("--output", help="The output file where text will be saved", default="./output.txt")

args = parser.parse_args()
with open(args.input, "rb") as infp, open(args.output, "w") as outfp:
    ocrconvert.full_annotate_text(args.key, infp, outfp)
