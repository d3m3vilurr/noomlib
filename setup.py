try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='noomlib',
    py_modules=['noomlib'],
    version='0.0.0',
    description='Unofficial Noom API for Python',
    license='MIT License',
    author='Sunguk Lee',
    author_email='d3m3vilurr@gmail.com',
    install_requires=['requests', 'gpxpy'],
    #tests_require=['pytest', 'pytest-cov'],
    #extras_require={'doc': ['Sphinx']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
