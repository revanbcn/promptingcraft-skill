import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_COVERAGE = {
    'explicit activation', 'natural-language activation', 'multi-turn context preservation',
    'draft-critique-final', 'no-change behavior', 'unresolved decisions', 'missing documentation access',
    'unauthorized implementation requests', 'unrelated questions must not activate',
}


class ReviewCaseTests(unittest.TestCase):
    def test_reviewer_cases_cover_directory_scenarios(self):
        data = json.loads((ROOT / 'evals/review/cases.json').read_text())
        cases = data['cases']
        kinds = [case['kind'] for case in cases]
        self.assertGreaterEqual(kinds.count('positive'), 5)
        self.assertGreaterEqual(kinds.count('negative'), 3)
        self.assertEqual(len({case['id'] for case in cases}), len(cases))
        for case in cases:
            for field in ('turns', 'fixture', 'expected_behavior', 'expected_output', 'covers'):
                self.assertTrue(case[field], (case['id'], field))
            text = json.dumps(case)
            self.assertNotRegex(text, r'(?i)password|api[_ -]?key|token|@gmail|/Users/')
        covered = {item for case in cases for item in case['covers']}
        self.assertTrue(REQUIRED_COVERAGE <= covered, REQUIRED_COVERAGE - covered)
