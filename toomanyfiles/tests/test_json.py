from os import chdir
from tempfile import TemporaryDirectory
from toomanyfiles import json

def test_json():    
    with TemporaryDirectory() as tempdir:
        chdir(tempdir)
        json.create()
        r=json.load()
        assert len(r)==1,  "Json length incorrect"
        
