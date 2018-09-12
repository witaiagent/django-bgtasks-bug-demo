# django-bgtasks-bug-demo
Small demo to showcase a bug in django-background-tasks.

This app showcases a bug that was encountered in django-background-tasks. 

The task is that from a background task, we make an HTTP call that updates our database. The said changes are saved and the task
is removed from the database. But, the problem is that when the task is exiting, it crashes. 

**To reproduce:**

1. Standard setup - Run migrations, start server.
2. Make the request. 

```bash
curl "http://localhost:8000/async/" --header "Content-Type application/json" --request POST --data '[{"name":"async1"}, {"name": "async2"}]'
```

3. To see that the data is saved - run `curl "http://localhost:8000/list/"`.

**Stack trace of error**

```
Traceback (most recent call last):
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/django/db/backends/base/base.py", line 239, in _commit
    return self.connection.commit()
sqlite3.OperationalError: disk I/O error

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "manage.py", line 15, in <module>
    execute_from_command_line(sys.argv)
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/django/core/management/__init__.py", line 371, in execute_from_command_line
    utility.execute()
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/django/core/management/__init__.py", line 365, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/django/core/management/base.py", line 288, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/django/core/management/base.py", line 335, in execute
    output = self.handle(*args, **options)
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/background_task/management/commands/process_tasks.py", line 94, in handle
    if not self._tasks.run_next_task(queue):
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/background_task/tasks.py", line 134, in run_next_task
    return self._runner.run_next_task(self, queue)
  File "/usr/lib/python3.6/contextlib.py", line 52, in inner
    return func(*args, **kwds)
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/django/db/transaction.py", line 212, in __exit__
    connection.commit()
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/django/db/backends/base/base.py", line 261, in commit
    self._commit()
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/django/db/backends/base/base.py", line 239, in _commit
    return self.connection.commit()
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/django/db/utils.py", line 89, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/mnt/c/Users/abhishek.p/Desktop/fooapp/venv/lib/python3.6/site-packages/django/db/backends/base/base.py", line 239, in _commit
    return self.connection.commit()
django.db.utils.OperationalError: disk I/O error
```

**Footnote**

Looks like the final transaction commit of updating the task status fails, even though the write to DB succeeds. 
