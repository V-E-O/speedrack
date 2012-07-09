About
-----

What's a *speedrack*? At a bar or food service event, the most common mixins are kept at arm-level, for efficiency -- this is the speedrack. Every reach is lost time, strain, and the line gets longer. Likewise, every reach for data or regular task execution, the line's getting longer. And like a lot of geeks, I'll work three days to save myself three minutes during crunch times. It's nice when things just work.

Ingredients
~~~~~~~~~~~

Speedrack is made from Flask_, `Twitter Bootstrap`_, and APScheduler_.

Contributing
~~~~~~~~~~~~

Some notes to hopefully save some effort on everyone's part.

- *Bugs*: love to hear about them!
- *Simple contributions* (known bugs, docs, typos, tweaks): just fork and request pull (tests <3)
- *Complex contributions* (new features): *email first*
- *Suggestions to do it right*: No thanks!


Gratitute and Inspiration
~~~~~~~~~~~~~~~~~~~~~~~~~

The good parts of this Flask application drew on knowledge and practices that `Andrew Roberts`_ and I accumulated in our work together. He's excellent; the bad parts are all mine.

Speedrack was inspired by Pydog_, by Philip Montgomery. My team used Pydog happily for years, but as our reliance on it grew, we needed something a little more stable. We already loved Flask_, so it was an easy choice.

.. _`Twitter Bootstrap`: http://twitter.github.com/bootstrap
.. _Pydog: http://pydog.sourceforge.net
.. _Flask: http://flask.pocoo.org
.. _APScheduler: http://packages.python.org/APScheduler/
.. _`Andrew Roberts`: https://github.com/aroberts

Alternatives
------------

Please, play the field. This solution works well for my team, but you should look at what else is out there.

For example, if you have a group of machines you'd like to run tasks on, please investigate `Celery`_ or `RQ`_ -- they're both quality work. There are countless alternatives, and most of them are probably better than this.

Speedrack is trivial to set up and administer. It runs well on one node. It's a good bad solution.

.. _Celery: http://celeryproject.org
.. _RQ: http://nvie.github.com/rq
