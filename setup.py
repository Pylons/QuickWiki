try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='QuickWiki',
    version="0.1.5",
    description="QuickWiki - Pylons 0.9.6 Tutorial application",
    #author="",
    #author_email="",
    url="http://wiki.pylonshq.com/display/pylonsdocs/QuickWiki+Tutorial",
    install_requires=["Pylons>=0.9.6", "docutils==0.4", "SQLAlchemy>=0.4.0beta5"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'quickwiki': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'quickwiki': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    entry_points="""
    [paste.app_factory]
    main = quickwiki.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
