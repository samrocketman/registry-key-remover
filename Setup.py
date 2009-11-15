from distutils.core import setup
import py2exe
# Filled out required information for setup.py from http://docs.python.org/distutils/setupscript.html
setup(name="Registry Key Remover",
      #Version = Major.Minor.PatchSet
      version="0.1.42",
      description="Removes registry keys based on the snap shot provided by RegShot.",
      url="https://sourceforge.net/projects/registrykeyremo/",
      author="coreyfournier, mpvenable, sag47",
      author_email="@users.sourceforge.net",
      console=['src/Reverter/__init__.py'])