import os
from setuptools import (
    setup,
    find_packages,
)


version = '0.1.dev0'
shortdesc = 'jQuery File Upload integration for cone.app'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()


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
    extras_require = dict(
        test=[
            'interlude',
            'plone.testing',
            'unittest2',
        ],
    ),
    tests_require=[
        'interlude',
        'plone.testing',
        'unittest2',
    ],
    test_suite = "cone.fileupload.tests.test_suite",
    entry_points="""\
    """
)
