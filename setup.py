import os, glob, sys, subprocess

VENV_DIRECTORY = 'env'
VENV_PROMPT = '[higgsml] '
ACTIVATE_LINK = 'activate'
REQUIREMENTS = 'requirements/requirements*.txt'

# Check the python version
major = sys.version_info[0]
minor = sys.version_info[1]
patch = sys.version_info[2]
if (major == 2 and minor < 7 and patch < 9) or (major < 2):
    print('Requires at least Python 2.7.9')
    sys.exit(1)

def create_venv():
    opts = ['virtualenv',
            '--prompt={}'.format(VENV_PROMPT),
            '--python={}'.format(sys.executable),
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
