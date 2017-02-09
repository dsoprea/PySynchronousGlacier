import os

import boto.glacier.exceptions

import sg.resource
import sg.job
import sg.archive
import sg.vault


class Helper(object):
    def __init__(self, ar):
        self.__ar = ar

    def delete_vault(self, vault_name, job_id=None):
        "Delete archives and then delete vault."

        j = sg.job.Job(self.__ar)

        if job_id is None:
            job_id = j.new_job_retrieve_inventory(vault_name)

        r = j.wait_on_job(vault_name, job_id)
        a = sg.archive.Archive(self.__ar)

        print("Deleting ({}) archives.".format(len(r['ArchiveList'])))

        for i, archive in enumerate(r['ArchiveList']):
            archive_id = archive['ArchiveId']
            description = archive['ArchiveDescription']

            print("Requesting archive delete: ({}) [{}]".format(i, description))
            a.delete(vault_name, archive_id)

        print("Attempting to delete vault: {}".format(vault_name))

        v = sg.vault.Vault(self.__ar)

        def cb():
            v.delete(vault_name)

        # Retry every minute.
        retry_interval_s = 60 * 1

        # Keep trying for one day.
        max_attempts = 60 * 24

        r = sg.common.auto_retry(
                'delete_vault',
                cb,
                'Vault not empty or recently written to:',
                retry_interval_s=retry_interval_s,
                max_attempts=max_attempts)
