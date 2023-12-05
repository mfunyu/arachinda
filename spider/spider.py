#!/usr/bin/env python3
import argparse
import requests
import re
import os

exts = [".jpg", ".jpeg", ".png", ",gif", ".bmp"]
links_visited = set()

def form_url(url, base):
	print(url, base)
	if url.startswith("http"):
		return url
	if base.startswith('//'):
		return base + url[:1]
	if not url.startswith('/'):
		return base + '/' + url
	return base + url

def download_images(url, directory, images):
	init = False

	pattern = re.compile(fr'.*({"|".join(re.escape(ext) for ext in exts)})$')
	for i_url in images:
		if not pattern.match(i_url):
			continue
		print(i_url)
		i_url = form_url(i_url, url)
		content = request(i_url)
		if not content:
			continue
		filename = directory + i_url[len(url) + 1:].replace('/', '-')
		if not init and not os.path.exists(directory):
			os.makedirs(directory)
			init = True
		with open(filename, 'wb') as f:
			f.write(content)

def request(url):
	try:
		#print("GET", url)
		r = requests.get(url)
	except requests.exceptions.ConnectionError:
		print("ERROR: connection refused - ", url)
		return
	if r.status_code != 200:
		print("ERROR:", url, r)
		return
	return r.content

def is_valid_link(href):
	if href.startswith('#'):
		return False
	if href.startswith("ftp:"):
		return False
	if href.startswith("tel:"):
		return False
	if href.startswith("javascript:"):
		return False
	if href.startswith("mailto:"):
		return False
	return True

def spider(url, loop, dir):
	c = str(request(url))
	images = re.findall(r'<img[^>]+src="(.*?)"', c)
	base = re.search(r'^(https?://[^/]+)', url).group()
	download_images(base, dir, images)

	if loop:
		urls = re.findall(r'<a[^>]+href="(.*?)"', c)
		for url in urls:
			if not is_valid_link(url):
				continue
			if url in links_visited:
				continue
			links_visited.add(url)
			url = form_url(url, base)
			spider(url, loop - 1, dir)

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("url", metavar="URL", type=str)
	parser.add_argument("-r", action="store_true")
	parser.add_argument("-l", default=5, type=int)
	parser.add_argument("-p", default="./data/", type=str)
	args = parser.parse_args()
	if not args.r:
		args.l = 0
	if not args.url.startswith('http'):
		print("ERROR:", url)
		exit(1)
	if args.url.endswith('/'):
		args.url = args.url[:-1]

	return args

def main():
	args = parse_args()
	spider(args.url, args.l, args.p)
	print(links_visited)

main()
