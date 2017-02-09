import time
import datetime

import boto.glacier.layer1

_POLL_DELAY_S = 60 * 1
_ANNOUNCE_INTERVAL_S = 60 * 10


class Job(object):
    def __init__(self, ar):
        self.__ar = ar

    def new_job_retrieve_inventory(self, vault_name, sns_topic_name=None):
        job_id = self.__new_job(
            vault_name, 
            'inventory-retrieval', 
            sns_topic_name=sns_topic_name)

        return job_id

    def __new_job(self, vault_name, type_name, job_data=None, sns_topic_name=None):
        if job_data is None:
            job_data = {
                'Type': type_name,
            }
        else:
            job_data['Type'] = type_name,

        if sns_topic_name is not None:
            job_data['SNSTopic'] = sns_topic_name

        l1 = self.__ar.get_l1()
        r = l1.initiate_job(vault_name, job_data)
        job_id = r['JobId']

        return job_id

    def wait_on_job(self, vault_name, job_id):
        l1 = self.__ar.get_l1()

        start_time = time.time()
        last_announce = None

        while 1:
            try:
                r = l1.get_job_output(vault_name, job_id)
            except boto.glacier.exceptions.UnexpectedHTTPResponseError as e:
                if ('The job is not currently available for download:' in e.message) is False:
                    raise
            else:
                return r

            run_time = time.time() - start_time

            hours = int(run_time // 3600)
            minutes = int((run_time % 3600) // 60)
            seconds = int(run_time - minutes * 60)

            now = datetime.datetime.now()
            if last_announce is None or (now - last_announce).total_seconds() > _ANNOUNCE_INTERVAL_S:
                print("Sleeping (running {:02d}:{:02d}:{:02d}).".format(hours, minutes, seconds))
                last_announce = now

            time.sleep(_POLL_DELAY_S)

        return r
