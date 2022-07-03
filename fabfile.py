from fabric import task
from datetime import date
from sys import platform
import os, subprocess

BASE_PATH = os.path.dirname(__file__)
GUIDE_FOLDER = "doc"
GUIDE_PATH = BASE_PATH + "/" + GUIDE_FOLDER 
default_hosts = ["localhost"]

@task(hosts=default_hosts)
def usage(c):
    print("usage: fab make_doc|publish_doc")

@task(hosts=default_hosts)
def pytest(c):
    #with lcd(GUIDE_PATH):
    with c.prefix('cd %s' % GUIDE_PATH):
        build_cmd = 'make clean html'
        c.local(build_cmd)

@task(hosts=default_hosts)
def unittest(c):
    cmd = "python3 test/test_rtcp_packet.py"
    c.local(cmd)