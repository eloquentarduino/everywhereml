from distutils.core import setup

packages=PACKAGES
data=TEMPLATES

setup(
  name='everywhereml',
  packages=packages,
  version='VERSION',
  license='MIT',
  description='Train ML in Python, run everywhere',
  author='Simone Salerno',
  author_email='eloquentarduino@gmail.com',
  url='https://github.com/eloquentarduino/everywhereml',
  download_url='https://github.com/eloquentarduino/everywhereml/blob/master/dist/everywhereml-VERSION.tar.gz?raw=true',
  keywords=[
    'ML',
    'machine learning'
  ],
  install_requires=[
    'numpy',
    'scikit-learn',
    'Jinja2',
    'cached-property',
  ],
  package_data={
    'everywhereml': data
  },
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Code Generators',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)