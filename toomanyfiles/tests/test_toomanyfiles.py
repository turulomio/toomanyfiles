from os import path
from tempfile import TemporaryDirectory
from toomanyfiles import toomanyfiles

def test_examples():
    toomanyfiles.create_examples()
    dir="toomanyfiles_examples/directories/"
    toomanyfiles.toomanyfiles(dir,  remove=False)
    toomanyfiles.toomanyfiles(dir,  remove=True)

    dir="toomanyfiles_examples/files/"
    toomanyfiles.toomanyfiles(dir,  remove=False)
    toomanyfiles.toomanyfiles(dir,  remove=True)
    
    dir="toomanyfiles_examples/files_with_different_roots/"
    toomanyfiles.toomanyfiles(dir,  remove=False)
    toomanyfiles.toomanyfiles(dir,  remove=True)
    toomanyfiles.remove_examples()

def test_date_pattern():
    with TemporaryDirectory() as tempdir:
        toomanyfiles.create_file(f"{tempdir}/20250101 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250102 Hola.doc")
        toomanyfiles.create_file(f"{tempdir}/20250201 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250202 Hola.xlsx")
       
        toomanyfiles.toomanyfiles(tempdir,  remove=True, time_pattern="%Y%m%d",  too_young_to_delete=0)

        assert path.exists(f"{tempdir}/20250101 Hola.xlsx")
        assert path.exists(f"{tempdir}/20250102 Hola.doc")
        assert path.exists(f"{tempdir}/20250201 Hola.xlsx")
        assert path.exists(f"{tempdir}/20250202 Hola.xlsx")
        
#    
#def toomanyfiles(remove, time_pattern="%Y%m%d %H%M", file_patterns="",  too_young_to_delete=30, max_files_to_store=100000000, remove_mode="RemainFirstInMonth", disable_log=False):
#    """
def test_main():
    toomanyfiles.main(["--pretend"])
