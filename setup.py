import os, glob, sys, subprocess

VENV_DIRECTORY='env'
VENV_PROMPT='higgsml'
ACTIVATE_LINK='activate'
REQUIREMENTS='requirements/requirements*.txt'

def create_venv():
    opts = ['virtualenv',
            '--prompt={}'.format(VENV_PROMPT),
            VENV_DIRECTORY]
    try:
        subprocess.call(opts)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print('Can\'t find virtualenv. Make sure virtualenv ' +
                  'is installed before running this script.')
            sys.exit(1)
        else:
            raise

def create_link():
    print('Making symbolic links...')
    try:
        os.remove(ACTIVATE_LINK)
        print('Replacing old link.')
    except OSError:
        pass
    os.symlink('{}/bin/activate'.format(VENV_DIRECTORY), ACTIVATE_LINK)

def install_requirements():
    print('Installing packages...')
    this_pip = '{}/bin/pip'.format(VENV_DIRECTORY)
    try:
        for requirements_file in sorted(glob.iglob(REQUIREMENTS)):
            subprocess.call([this_pip,
                             'install',
                             '--upgrade',
                             '-r', requirements_file])
    except (KeyboardInterrupt, SystemExit):
        raise # Allow the exception to actually stop the control flow
    print('Installation complete.')

def show_final_message():
    print
    print('To activate the {} environment, run'.format(VENV_PROMPT))
    print('\t source {}'.format(ACTIVATE_LINK))
    print('from this directory ({}).'.format(os.getcwd()))
    print

if __name__ == '__main__':
    create_venv()
    create_link()
    install_requirements()
    show_final_message()
