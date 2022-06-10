import os

if __name__ == '__main__':
    os.system('coverage run -m unittest discover -p "Test*.py"')
    os.system('coverage html --omit=*testing*,*init*,*emoji/*,analyzer/Analyzer.py')
    os.system('.\\htmlcov\\index.html')
