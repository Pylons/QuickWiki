"""Setup the QuickWiki application"""
import logging

from quickwiki.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup quickwiki here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Load the models
    from quickwiki.model import meta
    meta.metadata.bind = meta.engine

    # Create the tables if they aren't there already
    log.info("Creating tables...")
    meta.metadata.create_all(checkfirst=True)
    log.info("Successfully set up.")
    
    import quickwiki.model as model
    log.info("Adding front page data...")
    page = model.Page()
    page.title = u'FrontPage'
    page.content = u'Welcome to the QuickWiki front page.'
    meta.Session.add(page)
    meta.Session.commit()
    log.info("Successfully set up.")
