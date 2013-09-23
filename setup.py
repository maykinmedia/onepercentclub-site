#!/usr/bin/env python
import os
import sys

import bluebottle
from setuptools import setup, find_packages


def read_file(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

   
readme = read_file('README.rst')
changes = ''
#changes = read_file('CHANGES.rst')


install_requires = [
    'Babel==1.3',
    'BeautifulSoup==3.2.1',
    'Django==1.5.4',
    'Jinja2==2.7',
    #'MarkupSafe==0.18',
    'Pillow==2.1.0',
    #'Pygments==1.6',
    'South==0.8.1',
    'Sphinx==1.2b1',
    #'amqp==1.0.12',
    #'anyjson==0.3.3',
    #'billiard==2.7.3.30',
    #'celery==3.0.20',
    #'colorama==0.2.5',
    'cssmin==0.1.4',
    #'distribute==0.7.3',
    'django-admin-tools==0.5.1',
    #'django-appconf==0.6',
    'django-celery==3.0.17',
    #'django-choices==1.1.11',
    'django-compressor==1.2',
    'django-countries==1.5',
    'django-debug-toolbar==0.9.4',
    'django-docdata==0.1',
    'django-extensions==1.1.1',
    'django-filetransfers==0.0.0',
    'django-filter==0.6',
    'django-fluent-contents==0.9a1',
    'django-fluent-dashboard==0.3.2',
    'django-iban==0.2.1',
    'django-jenkins==0.14.0',
    'django-localflavor==1.0',
    'django-polymorphic==0.5',
    'django-registration==0.8',
    'django-salesforce==0.1.6.3',
    'django-social-auth==0.7.23',
    'django-statici18n==0.4.5',
    #'django-tag-parser==1.0.0',
    'django-taggit==0.10a1',
    'django-taggit-autocomplete-modified==0.1.0b4',
    #'django-template-analyzer==1.1.0',
    'django-templatetag-handlebars==1.2.0',
    'django-tinymce==1.5.1b2',
    'django-wysiwyg==0.5.1',
    'djangorestframework==2.3.6',
    'dkimpy==0.5.4',
    'dnspython==1.11.0',
    #'docutils==0.10',
    'html5lib==0.95',
    #'http-parser==0.8.1',
    #'httplib2==0.8',
    'jsmin==2.0.2',
    #'kombu==2.5.12',
    #'logilab-astng==0.24.3',
    #'logilab-common==0.59.1',
    'micawber==0.2.6',
    #'oauth2==1.5.211',
    #'py2exe==0.6.9',
    'pycurl==7.19.0',
    #'python-dateutil==2.1',
    #'python-openid==2.2.5',
    'pytz==2013b',
    'raven==3.3.12',
    'requests==1.2.3',
    #'restkit==4.2.1',
    'selenium==2.33.0',
    #'simplejson==3.3.0',
    #'six==1.3.0',
    #'socketpool==0.5.2',
    'sorl-thumbnail==11.12',
    'splinter==0.5.3',
    'suds-jurko==0.4.1.jurko.5.-development-',
    'surlex==0.1.2',
    'transifex-client==0.9',
]


dependency_links = [
    #'hg+ssh://hg@bitbucket.org/onepercentclub/suds@afe727f50704#egg=suds-jurko-0.4.1.jurko.5.-development-',
    'https://bitbucket.org/onepercentclub/suds/get/afe727f50704.zip#egg=suds-jurko-0.4.1.jurko.5.-development-',
    #'git+ssh://git@github.com/onepercentclub/django-salesforce.git@1e54beb7bcc15a893e9590fb27cbf08853da5599#egg=django-salesforce-0.1.6.3',
    'https://github.com/onepercentclub/django-salesforce/archive/1e54beb7bcc15a893e9590fb27cbf08853da5599.zip#egg=django-salesforce-0.1.6.3',
    #'hg+ssh://hg@bitbucket.org/onepercentclub/django-registration@ae9e9ed265ed#egg=django-registration-0.8',
    'https://bitbucket.org/onepercentclub/django-registration/get/ae9e9ed265ed.zip#egg=django-registration-0.8',
    #'hg+ssh://hg@bitbucket.org/wkornewald/django-filetransfers@32ddeac#egg=django-filetransfers-0.0.0',
    'https://bitbucket.org/wkornewald/django-filetransfers/get/32ddeac.zip#egg=django-filetransfers-0.0.0',
    #'git+ssh://git@github.com/onepercentclub/django-docdata.git@120ae5b8a1da6152d43d4601edc8832268e05515#egg=django-docdata-0.1',
    'https://github.com/onepercentclub/django-docdata/archive/120ae5b8a1da6152d43d4601edc8832268e05515.zip#egg=django-docdata-0.1',
]


tests_require = [
    'coverage==3.6',
    'django-nose==1.1',
    'mock==1.0.1',
    'nose==1.3.0',
    'pylint==0.28.0',
]


setup(
    name='bluebottle',
    version='.'.join(map(str, bluebottle.__version__)),
    license='BSD',

    # Packaging.
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=install_requires,
    dependency_links=dependency_links,
    tests_require=tests_require,
    include_package_data=True,
    zip_safe=False,

    # Metadata for PyPI.
    description='Bluebottle, the crowdsourcing framework initiated by the 1%CLUB.',
    long_description='\n\n'.join([readme, changes]),
    author='1%CLUB',
    author_email='info@onepercentclub.com',
    platforms=['any'],
    url='https://github.com/onepercentclub/bluebottle',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
    ],
)
