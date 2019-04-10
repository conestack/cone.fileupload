from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test
import os


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


version = '0.3.dev0'
shortdesc = 'jQuery File Upload integration for cone.app'
longdesc = '\n\n'.join([read_file(name) for name in [
    'README.rst',
    'LICENSE.rst'
]])


class Test(test):

    def run_tests(self):
        from cone.fileupload import tests
        tests.run_tests()


setup(
    name='cone.fileupload',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='node pyramid cone web',
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    url=u'https://github.com/bluedynamics/cone.fileuplaod',
    license='Simplified BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['cone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'cone.app',
    ],
    extras_require=dict(test=['zope.testrunner']),
    tests_require=['zope.testrunner'],
    cmdclass=dict(test=Test)
)
