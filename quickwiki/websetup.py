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

    log.info("Setting up database connectivity...")
    engine = config['pylons.g'].sa_engine
    log.info("Creating tables...")
    model.metadata.create_all(bind=engine)
    log.info("Successfully set up.")

    log.info("Adding front page data...")
    page = model.Page()
    page.title = 'FrontPage'
    page.content = 'Welcome to the QuickWiki front page.'
    model.Session.save(page)
    model.Session.commit()
    log.info("Successfully set up.")
