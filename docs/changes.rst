=======
Changes
=======

0.6.0
  added SCRIPT_NAME configuration variable for supporting sub-path server roots

0.5.2
  bugfix for APScheduler stale dependency and overambitious setup

0.5.1
  bugfix for sudo controls

0.5
  added in-app manual suspension of tasks, more convenient than commenting out task in yaml and reloading

0.4.1
  bugfix for spam_fail

0.4
  added spam_fail setting, for hammering failure messages

0.3.1
  added simple sudo controls

0.3.0
  fixed email and spam settings

0.2.11
  add params tab to show single-task execution criteria

0.2.10
  add single-file view

0.2.9
  reduce number of copied version strings
  add placeholder for tasks with no description

0.2.8
  standard numbering scheme

0.2.h
  use gevent if available, otherwise use Flask's development server
  gevent/libevent is no longer a hard requirement, and is not installed with speedrack

0.2.f
  convert docs to sphinx documentation and wire to readthedocs

0.2.e
  merge debug and config to one page 

0.2
  beta

0.1
  prototype/alpha
