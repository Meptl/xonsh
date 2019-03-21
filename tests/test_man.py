# -*- coding: utf-8 -*-
import os
import shutil
import xonsh

from xonsh.completers.man import complete_from_man

from tools import skip_if_on_windows

XONSH_PREFIX = xonsh.__file__
if "site-packages" in XONSH_PREFIX:
    # must be installed version of xonsh
    num_up = 5
else:
    # must be in source dir
    num_up = 2
for i in range(num_up):
    XONSH_PREFIX = os.path.dirname(XONSH_PREFIX)
PATH = (
    os.path.join(os.path.dirname(__file__), "bin")
    + os.pathsep
    + os.path.join(XONSH_PREFIX, "bin")
    + os.pathsep
    + os.path.join(XONSH_PREFIX, "Scripts")
    + os.pathsep
    + os.path.join(XONSH_PREFIX, "scripts")
    + os.pathsep
    + os.path.dirname(sys.executable)
    + os.pathsep
    + os.environ["PATH"]
)

skip_if_no_man = pytest.mark.skipif(
    shutil.which("man", path=PATH) is None, reason="man command not on PATH"
)

@skip_if_on_windows
@skip_if_no_man
def test_man_completion(monkeypatch, tmpdir, xonsh_builtins):
    tempdir = tmpdir.mkdir("test_man")
    monkeypatch.setitem(
        os.environ, "MANPATH", os.path.dirname(os.path.abspath(__file__))
    )
    xonsh_builtins.__xonsh__.env.update({"XONSH_DATA_DIR": str(tempdir)})
    completions = complete_from_man("--", "yes --", 4, 6, xonsh_builtins.__xonsh__.env)
    assert "--version" in completions
    assert "--help" in completions
