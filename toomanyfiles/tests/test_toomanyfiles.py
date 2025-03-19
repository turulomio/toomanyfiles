from os import chdir
from toomanyfiles import toomanyfiles
from pytest import raises ,  fixture


@fixture(autouse=True)
def run_around_tests():
    """Setup and teardown before and after each test."""
    print("\n-- Creating examples before test --")
    toomanyfiles.create_examples()
    yield  # this is where the testing happens
    print("\n-- Removing examples --")
    toomanyfiles.remove_examples()


def test_create_examples():
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
    
def test_main():
    toomanyfiles.main(["--pretend"])
