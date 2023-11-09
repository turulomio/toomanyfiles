from os import chdir
from toomanyfiles import toomanyfiles

def test_create_examples():
    toomanyfiles.create_examples()
    chdir("toomanyfiles_examples/directories/")
    toomanyfiles.toomanyfiles(remove=False)
    toomanyfiles.toomanyfiles(remove=True)
    chdir("../../toomanyfiles_examples/files/")
    toomanyfiles.toomanyfiles(remove=False)
    toomanyfiles.toomanyfiles(remove=True)
    
#    chdir("../../toomanyfiles_examples/files_with_different_roots/")
#    toomanyfiles.toomanyfiles(remove=False)
#    toomanyfiles.toomanyfiles(remove=True)
    chdir("../..")
    toomanyfiles.remove_examples()
