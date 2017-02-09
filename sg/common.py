import time
import datetime

import boto.glacier.exceptions

_RETRY_INTERVAL_S = 60 * 1
_ANNOUNCE_INTERVAL_S = 60 * 10
_MAX_ATTEMPTS = 0

def auto_retry(description, cb, loop_on_error_substring, retry_interval_s=_RETRY_INTERVAL_S, announce_interval_s=_ANNOUNCE_INTERVAL_S, max_attempts=_MAX_ATTEMPTS):
    print("Waiting for state change: [{}]".format(description))

    start_time = time.time()
    last_announce = None

    i = 0
    while i < max_attempts or max_attempts == 0:
        try:
            r = cb()
        except boto.glacier.exceptions.UnexpectedHTTPResponseError as e:
            if (loop_on_error_substring in e.message) is False:
                raise
        else:
            return r

        run_time = time.time() - start_time

        hours = int(run_time // 3600)
        minutes = int((run_time % 3600) // 60)
        seconds = int(run_time - hours * 3600 - minutes * 60)

        now = datetime.datetime.now()
        if last_announce is None or (now - last_announce).total_seconds() > announce_interval_s:
            print("{}: Waiting to retry (running {:02d}:{:02d}:{:02d}).".format(description, hours, minutes, seconds))
            last_announce = now

        i += 1
        time.sleep(retry_interval_s)

    raise Exception("All attempts failed: [{}]".format(description))
