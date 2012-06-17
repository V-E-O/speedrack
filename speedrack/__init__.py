version_info = (0, 1, "d")
version = '.'.join(str(n) for n in version_info[:3])
release = version + ''.join(str(n) for n in version_info[3:])

from flask import Flask
import os, sys
import filer

app = Flask(__name__)
# needed to make state saving work
app.secret_key = "not_so_secret_lololol"

# global application controls
app._shutdown = False
app._sched = None

from datetime import datetime
app.config['datetime_launch'] = datetime.now()

import signal
def sigint_handler(signal, frame):
    app.logger.warn("Received signal: " + str(signal))
    app._shutdown = True
    aps.shutdown(app._sched)
    app.logger.warn("Shutting down.")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)


def config_paths():
    '''Based on assigned settings, compute log, state, and job paths'''

    if not app.config.get("SPEEDRACK_DIR", None):
        warning_msg = """!!!!!\n"NOTE: using temp directory, please set SPEEDRACK_DIR in settings\n!!!!!\n"""
        sys.stdout.write(warning_msg)

        import tempfile
        default_temp_dir = tempfile.gettempdir()
        speedrack_instance_name = app.config.get("APP_NAME", "speedrack")
        default_speedrack_dir = os.path.join(default_temp_dir, speedrack_instance_name)
        app.config['SPEEDRACK_DIR'] = default_speedrack_dir

    def set_default_path(config_key, key_path):
        if not app.config.get(config_key) and app.config.get('SPEEDRACK_DIR'):
            key_dir = os.path.join(app.config.get('SPEEDRACK_DIR'), key_path)
            app.config[config_key] = key_dir
            print "setting {0} to {1}".format(config_key, key_dir)

    set_default_path("LOG_DIR", "logs")
    set_default_path("JOB_ROOT_DIR", "jobs")
    set_default_path("JOB_STATE", "speedrack.state")

def start_logger():

    app.debug_log_format = """%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s"""

    if not app.debug and app.config.get('LOG_DIR', None):
        # setup local log dir
        if not os.path.exists(app.config['LOG_DIR']):
            os.makedirs(app.config['LOG_DIR'])

        import logging
        from logging.handlers import RotatingFileHandler
        app.logger.setLevel(logging.DEBUG)

        handler = RotatingFileHandler("%(LOG_DIR)s/speedrack.log" % app.config,
                                      maxBytes=app.config['MAX_LOG_SIZE'],
                                      backupCount=app.config['LOG_COUNT'])
        handler.setLevel(logging.INFO)
        lines = {
            'first': " ".join(['%(asctime)-15s',
                               '%(levelname)-8s',
                               '%(pathname)s:%(lineno)d']),
            'second': "  %(message)s",
        }
        formatter = logging.Formatter("%(first)s\n%(second)s" % lines)
        handler.setFormatter(formatter)

        app.logger.addHandler(handler)

def launch_services():
    '''after settings have been loaded, start processes.'''

    # debug toolbar
    if app.config['FLASK_DEBUG_TOOLBAR']:
        app.debug = True
        app.config['SECRET_KEY'] = app.secret_key # looks in config rather than in global
        app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
        from flask.ext.debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app) # returns the toolbar; we don't need it

    start_logger()
    config_paths()
    filer.assert_no_tilde(app.config['JOB_ROOT_DIR'])
    if not os.path.exists(app.config['JOB_ROOT_DIR']):
        os.makedirs(app.config['JOB_ROOT_DIR'])
    start_scheduler()

def _set_settings_file(settings_file):
    """updates config with settings"""
    from werkzeug.utils import ImportStringError    
    try:
        app.config.from_pyfile(settings_file)
    except ImportStringError:
        sys.stderr.write("Received an ImportStringError, please review your python settings file\n%s\n" % settings_file)
        sys.exit(1)

def set_default_settings_file(settings_file):
    _set_settings_file(settings_file)

set_user_settings_file = set_default_settings_file

def set_task_file(task_file):
    """overrides demo task file"""
    app.config['CONFIG_YAML'] = task_file

import speedrack.context_processors
import speedrack.filters
import speedrack.views

from speedrack import models
from speedrack import timing
from speedrack import aps

def start_scheduler():
    app._sched = aps.init(app.config.get('CONFIG_YAML', None),
                          app.config.get('JOB_STATE', None))
    app.logger.info("Speedrack started in '%s' environment." % ("test"))
