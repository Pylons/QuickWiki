"""Setup the QuickWiki application"""
import logging

import pylons.test

from quickwiki.config.environment import load_environment
from quickwiki import model
from quickwiki.model.meta import Session, Base

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup {{package}} here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)
    
    # Create the tables if they don't already exist
    log.info("Creating tables...")
    Base.metadata.create_all(bind=Session.bind)
    log.info("Successfully set up.")
    
    log.info("Adding front page data...")
    page = model.Page(title=u'FrontPage',
                      content=u'**Welcome** to the QuickWiki front page!')
    Session.add(page)
    Session.commit()
    log.info("Successfully set up.")

