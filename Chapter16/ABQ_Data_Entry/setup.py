from setuptools import setup

with open('README.rst', 'r') as fh:
  long_description = fh.read()

setup(
  name='ABQ_Data_Entry',
  version='1.0',
  author='Alan D Moore',
  author_email='alandmoore@example.com',
  description='Data entry application for ABQ AgriLabs',
  url="http://abq.example.com",
  license='ABQ corporate license',
  long_description=long_description,
  packages=[
    'abq_data_entry',
    'abq_data_entry.images',
    'abq_data_entry.test'
  ],
  install_requires=[
      'requests', 'paramiko', 'matplotlib', 'psycopg2'
  ],
  python_requires='>=3.6',
  package_data={'abq_data_entry.images': ['*.png', '*.xbm']},
  entry_points={
    'console_scripts': [
      'abq = abq_data_entry.__main__:main'
    ]
  }
)
