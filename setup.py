"""
Setup for AWS Utils (Asyncio)
"""

from setuptools import setup


setup(name='aws-aioutils',
      version='1.0',
      description='AWS utilities (Asyncio)',
      url='https://github.com/merfrei/aws-aioutils',
      author='Emiliano M. Rudenick',
      author_email='contact@merfrei.com',
      license='MIT',
      packages=['aws'],
      install_requires=[
          'aioboto3',
      ],
      zip_safe=False)
