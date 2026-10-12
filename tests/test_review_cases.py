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


class TriggerQueryTests(unittest.TestCase):
    def test_trigger_queries_follow_the_description_optimization_method(self):
        queries = json.loads((ROOT / 'evals/trigger/queries.json').read_text())['queries']
        self.assertEqual(len({q['id'] for q in queries}), len(queries))
        for split, size in (('train', 12), ('validation', 8)):
            rows = [q for q in queries if q['split'] == split]
            self.assertEqual(len(rows), size)
            self.assertEqual(sum(q['should_trigger'] for q in rows), size // 2, split)
        for q in queries:
            self.assertNotRegex(q['query'], r'(?i)promptcraft|promptingcraft|\$|@')
