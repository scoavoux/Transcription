import sublime, sublime_plugin
import sys
import os
import time
from . import vlc
from . import yaml

#feed command to vlc socket to get the time played in seconds
workingdir = os.path.join(os.path.expanduser('~'))
vlcin = os.path.join(workingdir,'vlc.sock')
vlcout = os.path.join(workingdir,'vlc.out')

# audiofile = "/home/scoavoux/Dropbox/Thèse/Data/Observation-entretiens MBA/Enregistrements entretiens en salle/40 - 19072012 Femme, conservatrice, école du Louvre, Strasbourg - Benedicte Herbage.WAV"
# audiofile = "file://" + audiofile

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

	return(parsed_yaml)

# class TranscriptionGetFilePathCommand(sublime_plugin.TextCommand):
# 	def run(self,view):
# 		parsed_yaml = yamlparser(self.view)
# 		filename = parsed_yaml["file"]
# 		# filepath = "file"
# 		# Adjust for relative path
# 		return(filename)

# class VlcLaunchCommand(sublime_plugin.ApplicationCommand):
#     def run(self):
#     	filename = "/home/scoavoux/Dropbox/Thèse/Data/Observation-entretiens MBA/Enregistrements entretiens en salle/Thèse41 - 20072012 - Femme, employée banque de france, retraite (1).WAV"
#     	sublime.instance = vlc.Instance()
#     	sublime.mediaplayer = sublime.instance.media_player_new()
#     	sublime.media = sublime.instance.media_new(filename)
#     	sublime.mediaplayer.set_media(sublime.media)
		
# class VlcPlayCommand(sublime_plugin.ApplicationCommand):
# 	def run(self):
# 		sublime.mediaplayer.play()
# 		print("playing")
# 		time.sleep(5)
# 		sublime.mediaplayer.pause()
# 		print("stop playing")

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


## PARSE YAML
# Lire le nom du fichier dans le YAML

# Lire le nom des interlocuteurs.

# Set nombre interlocuteurs

## Lancer le fichier 

### TODO : garder en mémoire le temps.

# class VlcStartCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		self.instance = vlc.Instance()
#         self.mediaplayer = self.instance.media_player_new()
#         self.isPaused = False

# Lier un fichier son avec le fichier md.

# Contrôle de VLC : 
# 	+ lancer le fichier dans VLC (en arrière plan) ; 
# 	+ play/pause
# 	+ aller à temps
# 	+ avance rapide
# 	+ retour rapide
# 	+ monte/baisse son
# 	+ prends le temps

# Mode dictée à la 

# Liste d'interlocuteurs en YAML
# Insérer nom d'interlocuteur
# Si seulement deux interlocuteurs : changer d'interlocuteur à chaque double entrée
# Insérer time code formatté