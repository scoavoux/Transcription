import sublime, sublime_plugin
import sys
import os
from . import yaml

#feed command to vlc socket to get the time played in seconds
workingdir = os.path.join(os.path.expanduser('~'))
vlcin = os.path.join(workingdir,'vlc.sock')
vlcout = os.path.join(workingdir,'vlc.out')

def yamlparser(view):
	# look for yaml blocks
	yaml_position = view.find_all("---")
	
	# Make sure there is an even number of "---" (YAML blocks delimiter)
	if len(yaml_position)%2 == 1:
		print("Error : YAML blocks not defined properly")

	YAML = ""
	# Isolate YAML blocks
	for i in range(0,len(yaml_position),2):
		start = yaml_position[i].b
		stop = yaml_position[i+1].a
		YAML += view.substr(sublime.Region(start,stop))
		
	# Parse YAML Blocks
	parsed_yaml = yaml.load(YAML)

	return parsed_yaml


class VlcStartCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		os.system('echo "pause" | nc.openbsd -U ' + vlcin)

class VlcJogForwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		os.system('echo "key key-jump+extrashort" | nc.openbsd -U ' + vlcin)

class VlcJogBackwardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		os.system('echo "key key-jump-extrashort" | nc.openbsd -U ' + vlcin)

class TranscriptionNewLineCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		
		# define useful points
		view = self.view
		point = view.sel()[0].b
		line = view.substr(view.line(view.sel()[0]))
		
		parsed_yaml = yamlparser(view)

		# Extract Interviewer and Respondant names
		interviewer = parsed_yaml["interviewer"]
		respondant = parsed_yaml["respondant"]

		tagi = "> " + interviewer
		tagr = "> " + respondant

		if line[0:len(tagi)] == tagi:
		 	self.view.insert(edit, self.view.sel()[0].b, "\n\n> " + respondant + ": ")

		elif line[0:len(tagr)] == tagr:
		 	self.view.insert(edit, self.view.sel()[0].b, "\n\n> " + interviewer + ": ")

		else:
			print("You must be on a line beginning by '> interviewer' or '> respondant' for this awesome command to work")
