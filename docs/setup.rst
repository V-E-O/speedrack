Installation and Demo Mode
--------------------------

Speedrack requires *Python 2.6+*.

Please use virtualenv. If you've avoided it until now: it's really better. (If you don't have ``pip``, prepend the following instructions with: ``easy_install pip``)

::

    pip install speedrack
    speedrack run

Open a browser at ``localhost:8118``, see the demo tasks churning (can take a minute). Note that some of the test tasks are designed to fail (and often), to illustrate what failure would look like. Likewise with misconfigured tasks, and so on.

Don't expose this to the internet; **it's not even trying for security**.

Configuration
-------------

::

    speedrack init <target directory>

This will write two files to the target directory: ``speedrack_settings.py`` and ``speedrack_tasks.yaml``. They're the settings from the demo mode and are useful to build your tasks from.

Application settings
~~~~~~~~~~~~~~~~~~~~

``speedrack_settings.py`` contains *application behavior*: your application name, mail server settings, and so on. You won't need them all. If you're not familiar with python, you don't need to learn it to administer this application — just stick with the simple declarative syntax.

Task definitions and behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``speedrack_tasks.yaml`` defines each *task*: a shell command and schedule of execution. The sample file contains the tasks used for the demo you started with.

Running
-------

Once you've got your settings and tasks in place:

::

    speedrack run --settings speedrack_settings.py --tasks speedrack_tasks.yaml

Browse ``localhost:8118/config`` to check your active configuration at any time.