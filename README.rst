=========
SPEEDRACK
=========

Speedrack is a single-node cron system with an attractive web interface, job-tracking and configurable notification via email.

It is intended to drive regular executions of low-resource shell scripts, routing output to defined locations. The web front end makes it easy to see a high-level overview, which we've found works especially well for our small team.

Quick Installation and Local Demonstration
------------------------------------------

1. Start with python: http://www.python.org/download
2. (bonus: Use virtualenv_ (intermediate, recommended))
3. Install pip: ``easy_install pip``
4. Install speedrack: ``pip install speedrack``
5. Start speedrack: ``speedrack run``
6. Done! Check it out: ``http://localhost:8118``

.. _virtualenv: http://pypi.python.org/pypi/virtualenv

Speedrack comes with a demo mode, so look at your sample tasks churn. Results for these tasks are being pooled in your system temp directory.

**TODO: sphinx before publication**
For more information, please visit `speedrack's documentation`_. Did the demo? Jump right to `speedrack configuration`_.

.. _speedrack documentation: http://www.readthedocs.org/speedrack
.. _speedrack configuration: http://www.readthedocs.org/TODO

-----

**Sphinx stuff starts here**

Alternatives
------------

Please, play the field. This solution works well for my team, but you should look at what else is out there.

For example, if you have a group of machines you'd like to run tasks on, please investigate Celery_ or RQ_. They're both quality work. The purpose of Speedrack is to be trivial to set up and update, and fault-tolerant and \*reliable.

.. _Celery: http://celeryproject.org
.. _RQ: http://nvie.github.com/rq

Installation
------------

Speedrack requires *Python 2.6+*.

Please use virtualenv. If you've avoided it until now, please: it's really better. (If you don't have ``pip``, prepend the following instructions with: ``easy_install pip``)

::

    pip install speedrack
    speedrack run

Open a browser at ``localhost:8118``, see the demo tasks churning (can take a minute). Note that some of the test tasks are designed to fail (and often), to illustrate what failure would look like. Likewise with misconfigured tasks, and so on.

Don't expose this to the internet; **it's not even trying for security**. Likewise, don't make your crontab editable on your website, either.

Configuration
-------------

::

    speedrack init <target directory>

This will write two files to your local directory: ``speedrack_settings.py`` and ``speedrack_tasks.yaml``. I like to cut and paste from examples.

Application settings
~~~~~~~~~~~~~~~~~~~~

``speedrack_settings.py`` contains *application behavior*: your application name, mail server settings, and so on. You won't need them all. If you're not familiar with python, you don't need to learn it for this application — just stick with the simple declarative syntax.

Task definitions and behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``speedrack_tasks.yaml`` defines each *task*: a shell command and schedule of execution. The sample file contains the tasks used for the demo you started with.

Running
-------

Once you've got your settings and tasks in place:

::

    speedrack run --settings speedrack_settings.py --tasks speedrack_tasks.yaml

Browse ``localhost:8118/config`` to check your active configuration at any time.

Task Execution
--------------

Success / Failure
~~~~~~~~~~~~~~~~~

``FAIL_BY_NONZERO_STATUS_CODE`` and ``FAIL_BY_STDERR`` determine different indicators of task failure, both defaulted to true. Setting both of these to false will work, but you'll get less information in the task browser.

This is also configurable per task. You have to get the defaults / exceptions right.

Config Reloading
----------------

**TODO**

Speedrack asks APScheduler to shut down, and APScheduler waits for all current tasks to complete. This means that if you have a task that is going to take two hours to complete, it might be a while before Speedrack shuts down. Kill and restart Speedrack if you need it to reload right this second.

Scheduling
~~~~~~~~~~

Scheduling by Interval
^^^^^^^^^^^^^^^^^^^^^^

A simple joined string: ``1h10m`` means every one hour, ten minutes. Full vocabulary:

::

    { 'M': month, 'w': week, 'd': day, 'h': hour, 'm': minute, 's': second }

Don't forget that *interval* measures the time *between* complete executions -- a task that takes roughly ten minutes to complete with an interval of thirty minutes will kick off roughly every forty minutes, not every thirty minutes.

Scheduling by cron
^^^^^^^^^^^^^^^^^^

See APScheduler's documentation for `add\_cron\_job`_. In summary:

.. _`add_cron_job`: http://readthedocs.org/docs/apscheduler/en/latest/modules/scheduler.html#apscheduler.scheduler.Scheduler.add_cron_job

::

    year - year to run on
    month - month to run on
    day - day of month to run on
    week - week of the year to run on
    day_of_week - weekday to run on (0 = Monday)
    hour - hour to run on
    second - second to run on

Examples:

- ``{ "day_of_week": 2, "hour": 23 }``: Tuesdays at 23:00
- ``{ "day": 2, "hour": 23 }``: The 2nd of every month at 23:00
- ``{ "hour": 23 }``: Every day at 23:00


Run Now
^^^^^^^

Run Now behaves differently for interval and cron.

Using ``Run Now`` does not modify the next launch time. It schedules a parallel execution that happens *in addition* to your cron scheduling. Be aware of the following:

- Start at 00:00:00, cron set to every 30m.
- At 00:29:00, click ``Run Now``.
- At 00:30:00, Speedrack executes the scheduled task, perhaps in parallel with the manually submitted one.

Ingredients
-----------

Speedrack is made from Flask_, `Twitter Bootstrap`_, and APScheduler_.

Contributing
------------

Some notes to hopefully save some effort on everyone's part.

- *Bugs*: love to hear about them!
- *Simple contributions* (known bugs, docs, typos, tweaks): just fork and request pull (tests <3)
- *Complex contributions* (new features): *email first*

Random Notes
------------

Yes, it's built on minimally-configured `Twitter Bootstrap`_. This isn't customer-facing, and it's nice enough.

What's a *speedrack*? At a bar or food service event, the most common mixins are kept at arm-level, for efficiency -- this is the speedrack. Every reach is lost time, strain, and the line gets longer. Likewise, every reach for data or regular task execution, the line's getting longer. And like a lot of geeks, I'll work three days to save myself three minutes during crunch times. It's nice when things just work.

Thanks and Why
--------------

The good parts of this Flask implementation drew on knowledge and practices that `Andrew Roberts`_ and I accumulated in our work together. He's excellent; the bad parts are all mine.

Speedrack was inspired by Pydog_, by Philip Montgomery. My team used Pydog happily for years, but as our reliance on it grew, we needed something a little more stable. We already loved Flask_, so it was an easy choice.

.. _`Twitter Bootstrap`: http://twitter.github.com/bootstrap
.. _Pydog: http://pydog.sourceforge.net
.. _Flask: http://flask.pocoo.org
.. _APScheduler: http://packages.python.org/APScheduler/
.. _`Andrew Roberts`: https://github.com/aroberts
