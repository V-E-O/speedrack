import os.path

from nose.tools import *

from speedrack import models

TESTDATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")

SAMPLE_TASK = "sample_task"
SAMPLE_NO_EXECUTIONS = "sample_no_executions"
NOTIFICATION_TASK = "notification_test"

# Note that unlike default Task execution sorting, this
# is chronologically ascending
EXECUTIONS_GOOD = [
    "2012-05-03_18:40:44",
    "2012-05-03_18:41:44",
    "2012-05-03_18:42:44",
    "2012-05-03_18:43:44",
    "2012-05-03_18:44:44",
    "2012-05-03_18:45:44",
    "2012-05-03_18:46:44",
]
EXECUTION_BAD = "1955-10-05_12:55:55"

NOTIFICATION_EXECUTIONS = [
    "2002-05-03_18:00:00", # fail
    "2002-05-03_19:00:00", # fail
    "2002-05-03_20:00:00", # success
    "2002-05-03_21:00:00", # success
    "2002-05-03_22:00:00", # fail
]

class TestTaskList(object):

    def setup(self):
        self.tlist = models.TaskList(job_root_dir = TESTDATA_PATH)

    def test_get_from_disk(self):
        tasks = self.tlist.get()
        task_names = [x.name for x in tasks]
        assert_in(SAMPLE_NO_EXECUTIONS, task_names)
        assert_in(SAMPLE_TASK, task_names)

    def test_find_from_disk(self):
        task1 = self.tlist.find_task(SAMPLE_NO_EXECUTIONS)
        assert_equals(SAMPLE_NO_EXECUTIONS, task1.name)
        task2 = self.tlist.find_task(SAMPLE_TASK)
        assert_equals(SAMPLE_TASK, task2.name)

    def test_find_from_disk_none(self):
        task = self.tlist.find_task("no such task")
        assert_is_none(task)

    
class TestTask(object):

    def setup(self):
        self.t = models.Task(SAMPLE_TASK,
                             job_root_dir = TESTDATA_PATH)

    def test_has_execution(self):
        assert_true(self.t.has_executions())

    def test_count_executions(self):
        assert_equals(7, self.t.count_executions())

    def test_default_status_inactive(self):
        from speedrack import status
        assert_equals(status.INACTIVE, self.t.get_status())

    def test_find_execution_good(self):
        e = self.t.find_execution(EXECUTIONS_GOOD[0])
        assert_is_not_none(e)

    def test_find_execution_bad(self):
        e = self.t.find_execution(EXECUTION_BAD)
        assert_is_none(e)

    def test_find_previous_execution_good(self):
        e = self.t.find_previous_execution(EXECUTIONS_GOOD[1])
        assert_equals(e.timestamp, EXECUTIONS_GOOD[0])

    def test_find_previous_execution_bad_first(self):
        # First execution should have no previous execution
        e = self.t.find_previous_execution(EXECUTIONS_GOOD[0])
        assert_is_none(e)

    def test_find_previous_execution_bad_nomatch(self):
        # If we can't find the given execution, return None
        e = self.t.find_previous_execution(EXECUTION_BAD)
        assert_is_none(e)
        
    def test_get_last_execution(self):
        e = self.t.get_last_execution()
        assert_equals(e.timestamp, EXECUTIONS_GOOD[-1])


class TestExecution(object):

    def setup(self):
        execution_path = os.path.join(TESTDATA_PATH,
                                      SAMPLE_TASK,
                                      EXECUTIONS_GOOD[0])
        self.e = models.Execution(execution_path)

    def test_has_std_err(self):
        assert_false(self.e.has_std_err())

    def test_has_std_out(self):
        assert_true(self.e.has_std_out())

    def test_execution_error(self):
        assert_false(self.e.execution_error())

    def test_has_status_code(self):
        assert_true(self.e.has_status_code())


class TestNeedsNotification(object):

    def check_needs_notification(self, expected, args):
        assert_equal(expected,
                     models.needs_notification(*args))

    def setup(self):
        e0_path = os.path.join(TESTDATA_PATH,
                               SAMPLE_TASK,
                               EXECUTIONS_GOOD[0])
        self.e0 = models.Execution(e0_path)

        self.executions = []
        for ne in NOTIFICATION_EXECUTIONS:
            epath = os.path.join(TESTDATA_PATH, NOTIFICATION_TASK, ne)
            e = models.Execution(epath)
            self.executions.append(e)
            
    def test_initial_success_nospam(self):
        self.check_needs_notification(False, [self.e0, False])

    def test_initial_success_spam(self):
        self.check_needs_notification("success", [self.e0, True])

    def test_initial_failure_nospam(self):
        self.check_needs_notification("failed", [self.executions[0], False])

    def test_initial_failure_spam(self):
        self.check_needs_notification("failed", [self.executions[0], True])

    def test_failure_after_failure_nospam(self):
        self.check_needs_notification(False, [self.executions[1], False])

    def test_failure_after_failure_spam(self):
        self.check_needs_notification("failed", [self.executions[1], True])

    def test_success_after_failure_nospam(self):
        self.check_needs_notification("success", [self.executions[2], False])

    def test_success_after_failure_spam(self):
        self.check_needs_notification("success", [self.executions[2], True])

    def test_success_after_success_nospam(self):
        self.check_needs_notification(False, [self.executions[3], False])

    def test_success_after_success_spam(self):
        self.check_needs_notification("success", [self.executions[3], True])

    def test_failure_after_success_nospam(self):
        self.check_needs_notification("failed", [self.executions[4], False])

    def test_failure_after_success_spam(self):
        self.check_needs_notification("failed", [self.executions[4], True])


class TestIsConfError(object):

    def test_no_command(self):
        params = {
            'name':'name',
            'parsed_cron':True,
            'parsed_interval':True,
        }
        assert_true(models.is_conf_error(params))

    def test_no_name(self):
        params = {
            'command':'command',
            'parsed_cron':True,
            'parsed_interval':True,
        }
        assert_true(models.is_conf_error(params))

    def test_cron_and_interval(self):
        params = {
            'command':'command',
            'name':'name',
            'parsed_cron':True,
            'parsed_interval':True,
        }
        assert_true(models.is_conf_error(params))

    def test_cron_no_interval(self):
        params = {
            'command':'command',
            'name':'name',
            'parsed_cron':True,
        }
        assert_false(models.is_conf_error(params))

    def test_interval_no_cron(self):
        params = {
            'command':'command',
            'name':'name',
            'parsed_interval':True,
        }
        assert_false(models.is_conf_error(params))

    def test_no_timing(self):
        params = {
            'command':'command',
            'name':'name',
        }
        assert_true(models.is_conf_error(params))
