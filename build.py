import PyInstaller.__main__

PyInstaller.__main__.run([
    '--noconfirm',
    '--clean',
    '--onefile',
    '--add-data', 'static;static',
    'main.py'
])