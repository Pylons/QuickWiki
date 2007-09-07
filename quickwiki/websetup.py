"""Setup the QuickWiki application"""
import logging

from paste.deploy import appconfig
from pylons import config

from quickwiki.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup quickwiki here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    
    # Populate the DB on 'paster setup-app'
    import quickwiki.model as model

    print "Setting up database connectivity..."
    engine = config['pylons.g'].sa_engine
    print "Creating tables..."
    model.metadata.create_all(bind=engine)
    print "Successfully set up."

    print "Adding front page data..."
    page = model.Page()
    page.title = 'FrontPage'
    page.content = 'Welcome to the QuickWiki front page.'
    model.Session.save(page)
    model.Session.commit()
    print "Successfully set up."
