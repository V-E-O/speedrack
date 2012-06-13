# Application interface to APScheduler
from datetime import datetime, date, timedelta
import re

from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.shelve_store import ShelveJobStore
from apscheduler.triggers.interval import IntervalTrigger

import apscheduler.scheduler

from flask import flash

from speedrack import app
from speedrack import models
from speedrack import timing

logger = app.logger

# The handle of 'default' is necessary, or a default RAMStore is created
# which is pretty confusing
_FHANDLE = 'file'

# connect apscheduler's logger to application's
apscheduler.scheduler.logger = logger

def init(yaml_file, job_state_file = None):
    """Set up apscheduler, recover existing file store if there is one,
    otherwise kick off a new one with existing config settings"""

    sched = new_scheduler()
    if job_state_file:
        recover(sched, job_state_file)

    recovered_job_count = len(sched.get_jobs())
    if recovered_job_count == 0:
        logger.info("Recovered NO jobs from store, creating new job store and seeding with config-generated params.")
        sched = update(sched, yaml_file, job_state_file)
    else:
        logger.info("Recovered %d jobs from store." % recovered_job_count)

    if not sched.running:
        sched.start()

    return sched

def recover(sched, job_state_file):
    """Recovers existing persistent job store."""
    logger.debug("jobs before shelve recovery: %d" % len(sched.get_jobs()))
    logger.debug("jobs: " + str(sched.get_jobs()))
    job_store = ShelveJobStore(job_state_file)
    sched.add_jobstore(job_store, _FHANDLE)
    logger.debug("jobs after shelve recovery: %d" % len(sched.get_jobs()))
    logger.debug("jobs: " + str(sched.get_jobs()))

def new_scheduler():
    # each task needs to explicitly set itself as stateful
    apsched_config = { "coalesce": True }
    logger.debug("creating new scheduler")
    sched = Scheduler(apsched_config)
    return sched

def update(sched, yaml_file, job_state_file):
    """Clears existing persistent job store, replaces with new one
    created from current config file contents."""

    # the file-based scheduler store needs to be removed completely
    # to update any of its shelved settings:
    # http://readthedocs.org/docs/apscheduler/en/latest/index.html#job-persistency

    logger.info("Update requested, waiting on running jobs.")
    sched.shutdown()
    clear(sched)

    # Also, a given scheduler cannot be restarted once it's shut down.
    # So in essence, we're gracefully stopping the scheduler and
    # replacing it with a new one.
    sched = new_scheduler()

    yaml_config = models.Config(yaml_file)
    load_tasks(sched, yaml_config)
    sched.add_jobstore(ShelveJobStore(job_state_file), _FHANDLE)
    sched.start()
    return sched

def clear(sched):
    logger.info("Clear requested, removing filestore.")
    try:
        sched.remove_jobstore(_FHANDLE)
    except KeyError:
        logger.debug("No existing jobstore, skipping.")

def run_task(sched, task_name):
    '''Executes a given task immediately. In APScheduler, this is
    handled by adding a task in the very-near (1s) future. An
    interval-driven task has its interval reset with this execution. A
    cron-driven task does not. Returns True if successful.'''

    jobs = sched.get_jobs()

    target_job = None
    params = None
    for job in jobs:
        params = job.args[0]
        if params['name'] == task_name:
            target_job = job
            break

    if not target_job:
        logger.error("Couldn't find task [%s] in scheduler!" % task_name)
        return False

    if models.is_conf_error(params):
        logger.error("Can't execute task [%s] with configuration error" % task_name)
        return False

    # 1) adding 1s is such a hack, but if you add "now", then by the
    # time
    # 2) this explicitly is not set to use the filestore, but the
    # ramstore. this is not scheduled or repeating, and doubling up
    # the func/params seems to cause the function to always enter as
    # "repeating"
    sched.add_date_job(executor_func,
                       datetime.now() + timedelta(seconds=1),
                       args=[params])

    return True


def executor_func(params):
    '''Unpack parameters, construct Executor object, run function.'''

    name             = params['name']
    command          = params['command']
    config           = params['config']
    parsed_interval  = params['parsed_interval']
    parsed_cron      = params['parsed_cron']
    email_recipients = params.get('email_recipients', [])
    spam             = params.get('spam', None)
    description      = params.get('description', None)
    max_keep         = params.get('max_keep)', None)

    ex = models.Executor(name, command)
    ex.config = config
    if description:
        ex.description = description
    if max_keep:
        ex.max_keep = int(max_keep)
    if spam:
        ex.spam = spam
    ex.parsed_interval = parsed_interval
    ex.parsed_cron = parsed_cron
    ex.email_recipients = email_recipients
    ex.run()


def new_params(config_block):
    '''
    Converts a configuration block into parameters suitable
    for establishing a task.

    {
      'name': this name,
      'description': description,
      'max_keep': None,
    }
    '''

    logger.debug("new params requested: %s" % str(config_block))

    name = config_block.get('name', None)
    name = understate(name)
    description = config_block.get('description', None)
    max_keep = config_block.get('max_keep', None)
    command = config_block.get('command', None)

    email_recipients = config_block.get('email', None)
    if email_recipients:
        email_recipients = ",".split(email_recipients)
    else:
        email_recipients = []

    unparsed_interval = config_block.get('interval', None)
    parsed_interval = timing.parse_interval(unparsed_interval)

    unparsed_cron = config_block.get('cron', None)
    parsed_cron = timing.parse_cron(unparsed_cron)

    params = {
        'name': name,
        'description': description,
        'max_keep': max_keep,
        'command': command,
        'email_recipients': email_recipients,
        'parsed_cron': parsed_cron,
        'parsed_interval': parsed_interval,
        'config': config_block,
    }

    # In erroneous configurations, we add a dummy job with an
    # unrunnable* time so that we can display the errored
    # configuration to the user
    if models.is_conf_error(params):
        logger.warn("task %s has error:" % name)
        logger.warn(params)

    return params


def schedule_params(sched, params):
    '''Adds executor function to scheduler based on its members'''
    if models.is_conf_error(params):
        # using add_date_job as purgatory
        much_later = date.fromordinal(date.max.toordinal())
        sched.add_date_job(executor_func, much_later, args=[params], jobstore=_FHANDLE)
    elif params.get("parsed_interval", None):
        sched.add_interval_job(executor_func, args=[params], jobstore=_FHANDLE, **params["parsed_interval"])
    elif params.get("parsed_cron", None):
        sched.add_cron_job(executor_func, args=[params], jobstore=_FHANDLE, **params["parsed_cron"])
    else:
        raise Exception, "Shouldn't ever be here."


def load_tasks(sched, config):
    """Given a list of tasks, update the scheduler."""

    logger.debug("NUM TASKS: %d" % len(sched.get_jobs()))

    if config.parsed is None or len(config.parsed['tasks']) == 0:
        flash("Couldn't find any tasks in yaml.", "error")
        return

    for config_block in config.parsed['tasks']:
        params = new_params(config_block)
        schedule_params(sched, params)

def shutdown(sched):
    """Gracefully shutdown APScheduler."""
    logger.warn("Shutdown request received. Shutting down scheduler.")
    sched.shutdown()
    logger.warn("APScheduler shut down successfully.")


_disallowed_characters = r""" !@#$%^&\*(){}[]|'\""""
_disallowed_escaped = r"""[ !@#$%^&\*\(\){}\[\]\|'\"]+"""
def understate(name):
    ''' underscorify the given names '''
    name = name.lower()
    name = name.strip(_disallowed_characters)
    name = re.sub(_disallowed_escaped, r"_", name)
    return name
