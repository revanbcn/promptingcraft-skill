import json
import unittest
from pathlib import Path
class Smoke(unittest.TestCase):
    def test_policy_fields_remain_available_to_the_runtime(self):
        policy = json.loads(Path('manifest.json').read_text())['policy']
        self.assertEqual(policy['fields'], ['job_id', 'status'])
        self.assertEqual(policy['terminal'], 'failed_final')
