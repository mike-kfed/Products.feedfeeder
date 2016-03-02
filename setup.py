from setuptools import setup, find_packages

readme = open("README.rst").read().strip()
history = open("CHANGES.rst").read().strip()

setup(name='Products.feedfeeder',
      version='3.0',
      description="Turn external feed entries into Dexterity content items",
      long_description= readme + "\n\n" + history,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='feed rss atom',
      author='Zest Software',
      author_email='m.van.rees@zestsoftware.nl',
      url='https://github.com/collective/Products.feedfeeder',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'feedparser',
          'beautifulsoup4',
          'plone.app.dexterity',
      ],
      extras_require = {
          'test': [
              'Products.PloneTestCase',
              ],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
