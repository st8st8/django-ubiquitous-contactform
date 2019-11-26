from setuptools import setup
import subprocess
import os.path

long_description = (open('README.rst').read() +
                    open('CHANGES.rst').read() +
                    open('TODO.rst').read())

setup(
    name='django-ubiquitous-contactform',
    version='0.7.0',
    description='Ubiquitous contact form for django sites',
    author='Steve Bradshaw',
    author_email='steve@pcfive.co.uk',
    long_description=long_description,
    url='https://github.com/st8st8/django-ubiquitous_contactform/',
    packages=['ubiquitous_contactform', 'ubiquitous_contactform.migrations'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django 2+',
    ],
    zip_safe=False,
    test_suite='tests.runtests.runtests',
    package_data={'ubiquitous_contactform': [
                                 'templates/ubiquitous_contactform/emails/html/*',
                                 'templates/ubiquitous_contactform/emails/text/*',
                                 'templates/ubiquitous_contactform/*.html']}
)
