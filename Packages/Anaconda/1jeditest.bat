cd anaconda_lib
activate.bat  dev
python 
import jedi
print(jedi.Script('import pandas; df = pandas.DataFrame(); df.').completions())
print(jedi.Script('import pandas; pandas.').completions())