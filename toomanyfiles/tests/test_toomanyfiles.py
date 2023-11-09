from os import chdir
from toomanyfiles import toomanyfiles
from pytest import raises

def test_create_examples():
    toomanyfiles.create_examples()
    chdir("toomanyfiles_examples/directories/")
    toomanyfiles.toomanyfiles(remove=False)
    toomanyfiles.toomanyfiles(remove=True)
    chdir("../../toomanyfiles_examples/files/")
    toomanyfiles.toomanyfiles(remove=False)
    toomanyfiles.toomanyfiles(remove=True)
    
    chdir("../../toomanyfiles_examples/files_with_different_roots/")
    # This command will have exit code 2
    with raises(SystemExit) as e:
        toomanyfiles.toomanyfiles(remove=True)
    assert e.type == SystemExit
    assert e.value.code == 1    
    # This command will have exit code 2
    with raises(SystemExit) as e:
        toomanyfiles.toomanyfiles(remove=False)
    assert e.type == SystemExit
    assert e.value.code == 1
    chdir("../..")
    toomanyfiles.remove_examples()
    
def test_main():
    toomanyfiles.main(["--pretend"])
