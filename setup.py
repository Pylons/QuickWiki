from setuptools import setup, find_packages

setup(
    name='QuickWiki',
    version="0.1.3",
    description="Result of following the Pylons 0.9.4.1 Tutorial",
    url="http://www.pylonshq.com/docs/quick_wiki.html",
    author="James Gardner",
    #author_email="",
    install_requires=["Pylons==dev,>=0.9.4.1dev-r1772", "docutils==0.4", "SQLAlchemy>=0.2.6"],
    packages=find_packages(),
    include_package_data=True,
    test_suite = 'nose.collector',
    package_data={'quickwiki': ['i18n/*/LC_MESSAGES/*.mo']},
    entry_points="""
    [paste.app_factory]
    main=quickwiki:make_app
    [paste.app_install]
    main=pylons.util:PylonsInstaller
    """,
)
