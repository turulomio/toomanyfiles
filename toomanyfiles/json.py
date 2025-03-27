from gettext import translation
from json import dumps,  load as json_load
from importlib.resources import files

try:
    t=translation('toomanyfiles', files("toomanyfiles/") / 'locale')
    _=t.gettext
except:
    _=str
filename=".toomanyfiles.json"


def create(directory):
    r=[]
    r.append({
        "remove_mode": "RemainFirstInMonth", 
        "time_pattern":"%Y%m%d %H%M", 
        "file_regex_pattern": "", 
        "too_young_to_delete": 30, 
        "max_files_to_store": 1000000, 
        "disable_log": False, 
    })
    with open(directory +"/" +filename,  "w") as f:
        f.write(dumps(r,  indent=4,  sort_keys=True))
    
    
def load():
    try:
        with open(filename, 'r') as f:
            data = json_load(f)
        return data
    except FileNotFoundError:
        print(_("File '{0}' wasn't found.").format("filename"))
        return None
