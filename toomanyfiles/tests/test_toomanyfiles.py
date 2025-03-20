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
        assert not path.exists(f"{tempdir}/20250102 Hola.doc")
        assert path.exists(f"{tempdir}/20250201 Hola.xlsx")
        assert not path.exists(f"{tempdir}/20250202 Hola.xlsx")
        
    with TemporaryDirectory() as tempdir:
        toomanyfiles.create_file(f"{tempdir}/20250101 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250102 Hola.doc")
        toomanyfiles.create_file(f"{tempdir}/20250201 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250202 Hola.xlsx")
       
        toomanyfiles.toomanyfiles(tempdir,  remove=True, time_pattern="%Y%m%d",  too_young_to_delete=3)

        assert path.exists(f"{tempdir}/20250101 Hola.xlsx")
        assert path.exists(f"{tempdir}/20250102 Hola.doc")
        assert path.exists(f"{tempdir}/20250201 Hola.xlsx")
        assert path.exists(f"{tempdir}/20250202 Hola.xlsx")
        
    with TemporaryDirectory() as tempdir:
        toomanyfiles.create_file(f"{tempdir}/20250101 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250102 Hola.doc")
        toomanyfiles.create_file(f"{tempdir}/20250201 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250202 Hola.xlsx")
       
        toomanyfiles.toomanyfiles(tempdir,  remove=True, time_pattern="%Y%m%d",  too_young_to_delete=0,  max_files_to_store=1)

        assert not path.exists(f"{tempdir}/20250101 Hola.xlsx")
        assert not path.exists(f"{tempdir}/20250102 Hola.doc")
        assert path.exists(f"{tempdir}/20250201 Hola.xlsx")
        assert not path.exists(f"{tempdir}/20250202 Hola.xlsx")
        
                
def test_mixed_patterns():
    with TemporaryDirectory() as tempdir:
        toomanyfiles.create_file(f"{tempdir}/20250101 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250102 Hola.doc")
        toomanyfiles.create_file(f"{tempdir}/20250201 1000 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250202 Hola.xlsx")
       
        toomanyfiles.toomanyfiles(tempdir,  remove=True, time_pattern="%Y%m%d",  too_young_to_delete=0,  file_patterns=[])

        assert path.exists(f"{tempdir}/20250101 Hola.xlsx")
        assert not path.exists(f"{tempdir}/20250102 Hola.doc") 
        assert path.exists(f"{tempdir}/20250201 1000 Hola.xlsx") #Got datetime 20250201
        assert not path.exists(f"{tempdir}/20250202 Hola.xlsx")             
        
def test_mixed_files_and_dirs():
    with TemporaryDirectory() as tempdir:
        toomanyfiles.create_file(f"{tempdir}/20250101 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250102/20250102 Hola.doc")
        toomanyfiles.create_file(f"{tempdir}/20250201/20250201 1000 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250202 Hola.xlsx")
       
        toomanyfiles.toomanyfiles(tempdir,  remove=True, time_pattern="%Y%m%d",  too_young_to_delete=0,  file_patterns=[])

        assert path.exists(f"{tempdir}/20250101 Hola.xlsx")
        assert not path.exists(f"{tempdir}/20250102/20250102 Hola.doc") 
        assert path.exists(f"{tempdir}/20250201/20250201 1000 Hola.xlsx") #Got datetime 20250201
        assert not path.exists(f"{tempdir}/20250202 Hola.xlsx")
        
def test_date_pattern_with_filter():
    with TemporaryDirectory() as tempdir:
        toomanyfiles.create_file(f"{tempdir}/20250101 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250102 Hola.doc")
        toomanyfiles.create_file(f"{tempdir}/20250201 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250202 Hola.xlsx")
      
        toomanyfiles.toomanyfiles(tempdir,  remove=True, time_pattern="%Y%m%d",  too_young_to_delete=0,  file_patterns=["xlsx", "2025"])

        assert path.exists(f"{tempdir}/20250101 Hola.xlsx")
        assert path.exists(f"{tempdir}/20250102 Hola.doc") #Not selected due to file_patterns
        assert path.exists(f"{tempdir}/20250201 Hola.xlsx")
        assert not path.exists(f"{tempdir}/20250202 Hola.xlsx")
        
        
    with TemporaryDirectory() as tempdir:
        toomanyfiles.create_file(f"{tempdir}/20250101 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250102 Hola.doc")
        toomanyfiles.create_file(f"{tempdir}/20250201 Hola.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250202 Hola.xlsx")
       
        toomanyfiles.toomanyfiles(tempdir,  remove=True, time_pattern="%Y%m%d",  too_young_to_delete=0,  file_patterns=["doc"])

        assert path.exists(f"{tempdir}/20250101 Hola.xlsx")
        assert path.exists(f"{tempdir}/20250102 Hola.doc") 
        assert path.exists(f"{tempdir}/20250201 Hola.xlsx")
        assert path.exists(f"{tempdir}/20250202 Hola.xlsx")

def test_main():
    toomanyfiles.main(["--pretend"])
