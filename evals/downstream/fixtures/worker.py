"""Original isolated retry fixture; there is no scheduler or database."""


def retry_jobs(jobs):
    return [{'job_id': job['job_id'], 'delay': job['retry_delay']} for job in jobs]
