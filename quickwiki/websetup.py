import paste.deploy
from pylons.database import create_engine
import quickwiki.models as model

def setup_config(command, filename, section, vars):
    """
    Place any commands to setup quickwiki here.
    """
    conf = paste.deploy.appconfig('config:' + filename)
    paste.deploy.CONFIG.push_process_config({'app_conf':conf.local_conf,
                                             'global_conf':conf.global_conf})

    uri = conf['sqlalchemy.dburi']
    engine = create_engine(uri)
    print "Connecting to database %s" % uri
    model.meta.connect(engine)
    print "Creating tables"
    model.meta.create_all()

    print "Adding front page data"
    page = model.Page()
    page.title = 'FrontPage'
    page.content = 'Welcome to the QuickWiki front page.'
    page.flush()
    print "Successfully setup."
