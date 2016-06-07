import os, glob

VENV_DIRECTORY='env'
VENV_PROMPT='higgsml'
ACTIVATE_LINK='activate'
REQUIREMENTS='requirements/requirements*.txt'

os.system('virtualenv --prompt={} {}'.format(
    VENV_PROMPT, VENV_DIRECTORY))

print('Making symbolic links...')
try:
    os.remove(ACTIVATE_LINK)
    print('Replacing old link.')
except OSError:
    pass
os.symlink('{}/bin/activate'.format(VENV_DIRECTORY), ACTIVATE_LINK)

print('Installing packages...')
this_pip = '{}/bin/pip'.format(VENV_DIRECTORY)
for requirements_file in sorted(glob.iglob(REQUIREMENTS)):
    os.system('{} install --upgrade -r {}'.format(this_pip,
                                        requirements_file))
print('Installation complete.')
print
print('To activate the {} environment, run'.format(VENV_PROMPT))
print('\t source {}'.format(ACTIVATE_LINK))
print('from this directory ({}).'.format(os.getcwd()))
print
