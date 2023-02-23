from subprocess import Popen, PIPE, STDOUT
import sys


def test_commandline_installed():
    p = Popen(["phagetrix"], stdout=PIPE, stderr=STDOUT)
    out, _ = p.communicate()
    niceout = out.decode("utf-8")
    print(niceout)
    assert "Do the thing" in niceout
