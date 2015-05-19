__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$May 18, 2015 22:08:21 EDT$"


import os
import shutil
import subprocess
import tempfile
import time

from splauncher.core import main


class TestCore(object):
    def setup(self):
        self.cwd = os.getcwd()
        self.tempdir = ""
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

    def teardown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.tempdir)
        self.tempdir = ""
        self.cwd = ""

    def test_main_0(self):
        main("echo", "output")

        time.sleep(1.0)

        filenames = []
        for each_filename in os.listdir(self.tempdir):
            filenames.append(os.path.join(self.tempdir, each_filename))

        print os.listdir(os.path.expanduser("~"))
        print os.listdir("/")

        subprocess.call(["qstat"])

        assert ".err" in filenames[0]
        assert ".out" in filenames[1]

        with open(filenames[0], "r") as f:
            assert f.read() == ""

        with open(filenames[1], "r") as f:
            assert f.read() == "output"

    def test_main_1(self):
        main("echo", "error", "1>&2")

        time.sleep(1.0)

        filenames = []
        for each_filename in os.listdir(self.tempdir):
            filenames.append(os.path.join(self.tempdir, each_filename))

        print os.listdir(os.path.expanduser("~"))
        print os.listdir("/")

        subprocess.call(["qstat"])

        assert ".err" in filenames[0]
        assert ".out" in filenames[1]

        with open(filenames[0], "r") as f:
            assert f.read() == "error"

        with open(filenames[1], "r") as f:
            assert f.read() == ""