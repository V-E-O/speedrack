Installation and Demo Mode
--------------------------

Speedrack requires *Python 2.6+*. Python comes with easy_install.

(If you don't have ``pip``, prepend the following instructions with: ``easy_install pip``)

::

    pip install speedrack
    speedrack run

Open a browser at ``http://localhost:8118``, see the demo tasks churning (can take a minute). Note that some of the test tasks are designed to fail (and often), to illustrate what failure would look like. Likewise with misconfigured tasks, and so on.

Don't expose this to the internet; **it's not even trying for security**.

(If you have have libevent/`gevent`_ installed, Speedrack will run using that. Flask's dev server is fine, too.)

.. _gevent: http://www.gevent.org

Configuration
-------------

::

    speedrack init <target directory>

This will write two files to the target directory: ``speedrack_settings.py`` and ``speedrack_tasks.yaml``. They're the settings from the demo mode and are useful to build your tasks from.

Application settings
~~~~~~~~~~~~~~~~~~~~

``speedrack_settings.py`` contains *application behavior*: your application name, mail server settings, and so on. You won't need them all. If you're not familiar with python, you don't need to learn it to administer this application — just stick with the simple declarative syntax.

Sub-path support
----------------

If Speedrack is running at a non-root location on a domain (e.g., http://www.example.com/speedrack/ resolves to the application root view), then you'll need to let Speedrack know to modify the URLs it makes appropriately. In your configuration file, set the variable ``SCRIPT_NAME`` to whatever path prefix points to the Speedrack index (in this case, ``SCRIPT_NAME = '/speedrack'``).

.. note:: This setting alone does not actually change how Speedrack **parses** requests. Rather, this tells Speedrack that when it **generates** a URL, it should prefix it with the provided string. This means that when the client clicks a link or requests a stylesheet in the original response, the new request is pointed at the right location.

Task definitions and behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``speedrack_tasks.yaml`` defines each *task*: a shell command and schedule of execution. The sample file contains the tasks used for the demo you started with.

.. warning:: **Restrict access to this file.** Speedrack reads this file and executes the commands therein, *as the user who launched speedrack*. ``speedrack init`` gets the basic settings correct, but if you build your own, you should remove global write (and group, if necessary).

Running
-------

Once you've got your settings and tasks in place:

::

    speedrack run --settings speedrack_settings.py --tasks speedrack_tasks.yaml

Browse ``http://localhost:8118/config`` to check your active configuration at any time.
