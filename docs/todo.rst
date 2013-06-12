====
Todo
====

1.0
---

- more tests
- refactor models.Executor / Task / aps.executor_func

Future
------

- detect sanity of config variables to ensure no weird write failures
- "retain X previous failures", to prevent issues from being flushed out by successes in display
- add ability to list all jobs (or what, 100?) if asked instead of pithy message
- add users - no auth, just cookie for attribution
- run now improvements
  - store "manual execution" in job history / display? / store "executed by"?
- failure notification
  - raven / sentry
- live update of page? via pjax
  - 5s interval
