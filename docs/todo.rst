====
Todo
====

1.0
---

- more tests
- refactor models.Executor / Task / aps.executor_func

Future
------

- "retain X previous failures", to prevent issues from being flushed out by successes
- "config file updated" flag
  - upper right, with "reload"
  - your store was created X, config file updated later than X
- add ability to list all jobs (or what, 100?) if asked instead of pithy message
- run now improvements
  - store "manual execution" in job history / display?
  - store "executed by"?
- add users - no auth, just cookie for attribution
- fix tab implementation, is currently horrible
- failure notification
  - raven / sentry
- live update of page? via pjax
  - 5s interval
