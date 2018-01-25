##
# -*- coding: utf-8 -*-
# __main__.py
##

def setup():
	_settings = {
		'prefix': '!',
		'token': None,
		'message_ignore': [],
		'increment_score': True,
		'remove_default_help': True,
		'load_default': True,
	}

	with open('settings.json', 'w') as inf:
		json.dump(_settings, inf)

def main():
	operations = {
		'setup': setup,
		
	}
	for arg in sys.argv:
		if arg not in operations:
			print('Unrecognised command \'{0}\''.format(arg))
		else:
			operations[arg]()

if __name__ == '__main__':
	main()
