#!/usr/bin/env python3
import argparse


def validate_url(url):
	# ?

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("url", metavar="URL", type=str)
	parser.add_argument("-r", action="store_true")
	parser.add_argument("-l", default=5, type=int)
	parser.add_argument("-p", default="./data/", type=str)
	args = parser.parse_args()

	return args

def main():

	args = parse_args()
	print(args)

	validate_url(args.url)

main()
