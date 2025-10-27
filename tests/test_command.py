import os
from subprocess import PIPE, STDOUT, Popen


def test_commandline_installed():
    if os.name == "nt":
        return  # The following does not work as a test on windows

    p = Popen(["phagetrix"], stdout=PIPE, stderr=STDOUT)
    out, _ = p.communicate()
    niceout = out.decode("utf-8")
    print("=" * 5, "Output:")
    print(niceout)
    assert "following arguments" in niceout
