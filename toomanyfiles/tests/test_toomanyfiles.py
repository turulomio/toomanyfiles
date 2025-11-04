from datetime import datetime
from os import path
from tempfile import TemporaryDirectory
from toomanyfiles import toomanyfiles

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

def test_filename_with_time_pattern_in_directory_and_file():
    with TemporaryDirectory() as tempdir:
        newdir=f"{tempdir}/20251101"
        toomanyfiles.create_file(f"{newdir}/20251102 20620402.xlsx")
        toomanyfiles.create_file(f"{newdir}/20251103 20620402.xlsx")
        toomanyfiles.create_file(f"{newdir}/20251104 20620402.xlsx")
        toomanyfiles.create_file(f"{newdir}/20251105 20620402.xlsx")        
        
        toomanyfiles.toomanyfiles(newdir,  remove=True, time_pattern="%Y%m%d",  too_young_to_delete=0)

        assert path.exists(f"{newdir}/20251102 20620402.xlsx")
        assert not path.exists(f"{newdir}/20251103 20620402.xlsx") 
        assert not path.exists(f"{newdir}/20251104 20620402.xlsx")
        assert not path.exists(f"{newdir}/20251105 20620402.xlsx")
        
def test_filename_with_time_pattern_in_several_directories():
    with TemporaryDirectory() as tempdir:
        newdir=f"{tempdir}/20251101"
        toomanyfiles.create_directory(f"{newdir}/20251102 20620402")
        toomanyfiles.create_directory(f"{newdir}/20251103 20620402")
        toomanyfiles.create_directory(f"{newdir}/20251104 20620402")
        toomanyfiles.create_directory(f"{newdir}/20251105 20620402")        
        
        toomanyfiles.toomanyfiles(newdir,  remove=True, time_pattern="%Y%m%d",  too_young_to_delete=0)

        assert path.exists(f"{newdir}/20251102 20620402")
        assert not path.exists(f"{newdir}/20251103 20620402") 
        assert not path.exists(f"{newdir}/20251104 20620402")
        assert not path.exists(f"{newdir}/20251105 20620402")


def test_datetime_in_basename():
    assert toomanyfiles.datetime_in_basename("20250303 Hola.xlsx", "%y%m%d")==datetime(2025,3,3)
    assert toomanyfiles.datetime_in_basename("20251102 Hola 20620402.xlsx", "%y%m%d")==datetime(2025,11,2)