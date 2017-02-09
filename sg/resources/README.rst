-----------
Description
-----------

Glacier is meant for long-term storage of large files/archives. It is a time-consuming process to delete archives and download files. Additionally, you can not delete a Glacier vault container if it still contains archives.

In order to delete a vault, the normal process is:

- Create a job to evaluate the current contents of the vault.
- Wait until the job has been completed (usually three or four hours in us-east).
- Request the job output data.
- Delete each archive listed in the job-output.
- Delete the vault.

This can become obnoxious. The goal of this tool is to execute synchronous workflows that just stay running until the job is done.


-------
Install
-------

Install using PIP::

    $ sudo pip install synchronous_glacier


-----
Tools
-----

sg-vault-delete
===============

Executes the vault-deletion workflow.

Example output::

    $ sg-vault-delete ACCESSKEY SECRETKEY dustin-test-multi-3
    Watching job [76c9jSYmg6k9ZbgxdpZLtRq2kDZML_yzhU_1tEL1f_CgEiXjHyKnnoMTDVFciexsGM82k9X1v9K7T0ms-imt9SvPgPW0].
    Sleeping (running 00:00:00).
    Sleeping (running 00:10:03).
    Sleeping (running 00:20:07).
    Sleeping (running 00:30:11).
    Sleeping (running 00:40:15).
    Sleeping (running 00:50:19).
    ...
    Job complete. Deleting (3) archives.
    Requesting archive delete: (0) [dustin-test-archive1]
    Requesting archive delete: (1) [dustin-test-archive2]
    Requesting archive delete: (2) [dustin-test-archive3]
    Deleting vault: dustin-test-multi-3


-----
To Do
-----

We have only written one tool to solve one problem. PRs will be readily accepted to extend the project with additional tools to execute different workflows.
