from distutils.core import setup
import py2exe

setup(
    console=['INVOICERECO.py'],
    options={
        'py2exe': {
            'packages': ['pandas', 'numpy'],
            'includes': ['numpy.core._multiarray_tests'],
            'bundle_files': 1,
            'compressed': True
        }
    },
    zipfile=None
)
