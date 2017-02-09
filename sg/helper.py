import os

import sg.resource
import sg.job
import sg.archive
import sg.vault


class Helper(object):
    def __init__(self, ar):
        self.__ar = ar

    def delete_vault(self, vault_name):
        "Delete archives and then delete vault."

        j = sg.job.Job(self.__ar)
        
        job_id = os.environ.get('SG_JOB_ID')
        if job_id is None:
            job_id = j.new_job_retrieve_inventory(vault_name)

        print("Watching job [{}].".format(job_id))

        r = j.wait_on_job(vault_name, job_id)
        a = sg.archive.Archive(self.__ar)

        print("Job complete. Deleting ({}) archives.".format(len(r['ArchiveList'])))

        for i, archive in enumerate(r['ArchiveList']):
            archive_id = archive['ArchiveId']
            description = archive['ArchiveDescription']

            print("Requesting archive delete: ({}) [{}]".format(i, description))
            a.delete(vault_name, archive_id)

        print("Deleting vault: {}".format(vault_name))

        v = sg.vault.Vault(self.__ar)
        v.delete(vault_name)
