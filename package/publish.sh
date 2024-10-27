

python.exe setup.py bdist_wheel sdist
twine.exe upload -r testpypi dist/*
