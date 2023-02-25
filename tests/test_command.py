from subprocess import Popen, PIPE, STDOUT
import os


def test_commandline_installed():
    if os.name == "nt":
        return  # The following does not work as a test on windows

    p = Popen(["phagetrix"], stdout=PIPE, stderr=STDOUT)
    out, _ = p.communicate()
    niceout = out.decode("utf-8")
    print(niceout)
    assert "following arguments" in niceout
