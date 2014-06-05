import sublime, sublime_plugin
import sys
import os
from . import yaml
from .pydub import AudioSegment

# instance = vlc.Instance()
# mediaplayer = instance.media_player_new()
# media = instance.media_new(filename)
# mediaplayer.set_media(media)

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

# class TranscriptionGetFilePathCommand(sublime_plugin.TextCommand):
# 	def run(self,view):
# 		parsed_yaml = yamlparser(self.view)
# 		filename = parsed_yaml["file"]
# 		# filepath = "file"
# 		# Adjust for relative path
# 		print(parsed_yaml)
# 		return filename

# class VlcLaunchCommand(sublime_plugin.ApplicationCommand):
#     def run(self):
#     	filename = "/home/scoavoux/Dropbox/Thèse/Data/Observation-entretiens MBA/Enregistrements entretiens en salle/Thèse41 - 20072012 - Femme, employée banque de france, retraite (1).WAV"
		
# class VlcPlayCommand(sublime_plugin.ApplicationCommand):
# 	def run(self):
# 		sublime.mediaplayer.play()
# 		print("playing")
# 		time.sleep(5)
# 		sublime.mediaplayer.pause()
# 		print("stop playing")



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