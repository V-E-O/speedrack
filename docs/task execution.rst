Task Execution
==============

Scheduling
----------

Speedrack uses simple strings for *interval* (``1h10m``) and APScheduler's `add\_cron\_job`_ for *cron* scheduling (e.g. ``{ "day_of_week": 2, "hour": 23 }``. The most current documentation is in the app itself, under the Help tab.

Speedrack can launch jobs *immediately* via the Run Now button.

.. _`add_cron_job`: http://readthedocs.org/docs/apscheduler/en/latest/modules/scheduler.html#apscheduler.scheduler.Scheduler.add_cron_job

Success / Failure
-----------------

``FAIL_BY_NONZERO_STATUS_CODE`` and ``FAIL_BY_STDERR`` determine different indicators of task failure, both defaulted to true. Setting both of these to false will work, but you'll get less information in the task browser.

This is also configurable per task. The administrator is responsible for getting the defaults / exceptions right.

Sudo control
------------

Sudo execution requires the hosting user to have password-free sudo access to the given user. Commands will end up being roughly equivalent to:

    $ sudo -u task_sudo_user task_command

Config Reloading
----------------

When you reload the application via the web interface, Speedrack waits for all current tasks to complete. This means that if you have a task that is going to take two hours to complete, it might be a while before Speedrack shuts down. Kill and restart Speedrack if you need it to stop and reload right this second.
