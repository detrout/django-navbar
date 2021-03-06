from setuptools import setup, find_packages
import os

try:
    reqs = open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).read()
except (IOError, OSError):
    reqs = ''

setup(
    name='django-navbar',
    version=__import__('navbar').__version__,
    description='Reusable django application managing navigation menues with '
                'permissions, auto selection and crumbs.',
    long_description=open('docs/overview.txt').read(),
    author='Doug Napoleone',
    author_email='doug.napoleone@gmail.com',
    url='http://code.google.com/p/django-navbar/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    install_requires=reqs
)
