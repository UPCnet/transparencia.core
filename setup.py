from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='transparencia.core',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='core transparencia',
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://github.com/UPCnet/transparencia.core.git',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['transparencia'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'transparencia.theme',
          'plone.app.dexterity',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
