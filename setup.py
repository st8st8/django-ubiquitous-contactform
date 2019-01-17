from setuptools import setup
import subprocess
import os.path

long_description = (open('README.rst').read() +
                    open('CHANGES.rst').read() +
                    open('TODO.rst').read())

setup(
    name='django-myenquiries',
    version='1.0.0',
    description='Ubiquitous contact form for django sites',
    author='Steve Bradshaw',
    author_email='steve@pcfive.co.uk',
    long_description=long_description,
    url='https://github.com/st8st8/django-myenquiries/',
    packages=['myenquiries', 'myenquiries.templatetags', 'myenquiries.migrations'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    zip_safe=False,
    test_suite='tests.runtests.runtests',
    package_data={'myenquiries': [
                                 'templates/myenquiries/emails/html/*',
                                 'templates/myenquiries/emails/text/*',
                                 'templates/myenquiries/*.html'}
)
