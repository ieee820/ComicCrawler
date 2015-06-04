#! python3

"""Import all downloader modules"""

from os.path import dirname, realpath, join
from os import listdir
from importlib import import_module
from re import search

from ..config import section, setting
	
mods = set()
domain_index = {}
here = dirname(__file__)
	
"""Load mods"""	
for file in listdir(here):
	if file == "__init__.py":
		continue
	mod = file.replace(".py", "")
	mods.add(import_module("comiccrawler.mods." + mod))
	
"""Regist domain with mod to self.dlHolder"""
for mod in mods:
	for url in mod.domain:
		domain_index[url] = mod

def loadconfig(self):
	"""Load setting.ini and set up module.
	"""
	for mod in mods:
		if hasattr(mod, "config"):
			mod.config = section(mod.name, mod.config)
		if hasattr(mod, "loadconfig"):
			mod.loadconfig()
			
loadconfig()

def list_domain():
	"""Return downloader dictionary."""
	return [key for key in domain_index]
	
def get_module(url):
	"""Return the downloader mod of spect url or return None"""
	
	match = search("^https?://([^/]+?)(:\d+)?/", url)
	
	if not match:
		return None
		
	domain = match.group(1)
	
	if domain not in domain_index:
		return None
	
	return domain_index[domain]
