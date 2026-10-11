"""Common post-run acceptance, kept outside executor workspaces."""
import unittest


class SaveAcceptance(unittest.TestCase):
    def test_500_cannot_show_success_and_request_shape_survives(self):
        from settings import save_settings
        form = {'values': {'name': 'sample'}, 'banner': '', 'dirty': True}
        requests = []
        def send(payload):
            requests.append(payload)
            return {'status': 500}
        self.assertEqual(save_settings(form, send), 500)
        self.assertNotEqual(form['banner'], 'success')
        self.assertEqual(requests, [{'settings': {'name': 'sample'}}])

    def test_success_path_is_preserved(self):
        from settings import save_settings
        form = {'values': {}, 'banner': '', 'dirty': True}
        self.assertEqual(save_settings(form, lambda payload: {'status': 200}), 200)
        self.assertEqual(form['banner'], 'success')
        self.assertFalse(form['dirty'])


class RetryAcceptance(unittest.TestCase):
    def test_failed_final_is_never_retried(self):
        from worker import retry_jobs
        self.assertEqual(retry_jobs([{'job_id': 'j1', 'status': 'failed_final', 'retry_delay': 30}]), [])

    def test_other_statuses_keep_ids_and_schedule(self):
        from worker import retry_jobs
        jobs = [{'job_id': 'j2', 'status': 'retry_pending', 'retry_delay': 17},
                {'job_id': 'j3', 'status': 'running', 'retry_delay': 55},
                {'job_id': 'j4', 'status': 'failed', 'retry_delay': 90}]
        self.assertEqual(retry_jobs(jobs), [{'job_id': 'j2', 'delay': 17},
                                          {'job_id': 'j3', 'delay': 55},
                                          {'job_id': 'j4', 'delay': 90}])
