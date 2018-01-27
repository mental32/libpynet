##
# -*- coding: utf-8 -*-
##

def markdown(text, style=''):
	return '```{0}\n{1}```'.format(style, text)

def nice_time(seconds):
	get_min = lambda s: (s-((s//3600)*3600))/60
	if seconds < 60:
		return str(seconds)+'s'
	elif seconds < 3600:
		return str(seconds//60)+'m '+str(round(seconds%60, 2))+'s'
	else:
		return str(seconds//3600)+'h '+str(get_min(seconds))+'m'
