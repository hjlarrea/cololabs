"""Refuse accidental publication from a preview clone or unreviewed branch."""
import subprocess
import sys


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


def check():
    origin = git('remote', 'get-url', '--push', 'origin').removesuffix('.git')
    if origin not in ('git@github.com:hjlarrea/cololabs', 'https://github.com/hjlarrea/cololabs'):
        sys.exit('Publish only from a production clone with origin = hjlarrea/cololabs.')
    if git('branch', '--show-current') != 'main':
        sys.exit('Publish only from production main after merging the reviewed PR.')
    if git('status', '--porcelain'):
        sys.exit('Commit or stash all working-tree changes before publishing.')
    remote = git('ls-remote', 'origin', 'refs/heads/main').split()
    if not remote or git('rev-parse', 'HEAD') != remote[0]:
        sys.exit('Local main must match production origin/main. Pull before publishing.')
    print('Production publishing source verified.')


if __name__ == '__main__':
    check()
