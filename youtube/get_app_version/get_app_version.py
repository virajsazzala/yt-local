from __future__ import unicode_literals
from subprocess import (
    call,
    STDOUT
)
from ..version import __version__
import os
import subprocess


def app_version():
    def minimal_env_cmd(cmd):
        # make minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v

        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    subst_list = {
        "version": __version__,
        "branch": None,
        "commit": None
    }

    if os.system("command -v git > /dev/null 2>&1") != 0:
        subst_list
    else:
        if call(["git", "branch"], stderr=STDOUT,
                stdout=open(os.devnull, 'w')) != 0:
            subst_list
        else:
            # version
            describe = minimal_env_cmd(["git", "describe", "--always"])
            git_revision = describe.strip().decode('ascii')
            # branch
            branch = minimal_env_cmd(["git", "branch"])
            git_branch = branch.strip().decode('ascii').replace('* ', '')

            subst_list = {
                "version": __version__,
                "branch": git_branch,
                "commit": git_revision
            }

    return subst_list


if __name__ == "__main__":
    app_version()
