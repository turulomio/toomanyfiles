from cx_Freeze import setup
from recovermypartition import version
name="recovermypartition"


setup(name=name,
      version = version,
      author = 'Mariano Muñoz',
      author_email="turulomio@yahoo.es", 
      description = 'Search devices in my LAN',
      url="https://sourceforge.net/projects/recovermypartition/", 
      )
