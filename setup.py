import os

VENV_DIRECTORY='env'
VENV_PROMPT='higgsml'
ACTIVATE_LINK='activate'

os.system('virtualenv --prompt={} {}'.format(VENV_PROMPT, VENV_DIRECTORY))

print('Making symbolic links...')
os.symlink('{}/bin/activate'.format(VENV_DIRECTORY), ACTIVATE_LINK)
