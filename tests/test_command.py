from subprocess import Popen, PIPE, STDOUT

def test_commandline_installed():
    p = Popen(["phagetrix"], stdout=PIPE, stderr=STDOUT)
    out, _ = p.communicate()
    niceout = out.decode("utf-8")
    print(niceout)
    assert "following arguments" in niceout
