import json
import tempfile
import unittest
from pathlib import Path

from scripts.evaluate import select_cases, extract_handoff, parse_events


class EvaluationTests(unittest.TestCase):
    def test_default_selection_runs_every_planned_case(self):
        cases = [{'id': str(index), 'prompt': 'Example'} for index in range(10)]
        self.assertEqual(len(select_cases(cases)), 10)

    def test_unknown_ids_are_rejected_instead_of_silently_skipped(self):
        with self.assertRaises(ValueError):
            select_cases([{'id': 'small-bug'}], ['typo'])

    def test_only_complete_copyable_handoff_is_measured(self):
        text = 'Assumptions outside.\n```text\nFix Save. No deployment.\n```\nReview outside.'
        self.assertEqual(extract_handoff(text), 'Fix Save. No deployment.')

    def test_missing_or_multiple_blocks_remain_unresolved(self):
        self.assertIsNone(extract_handoff('No handoff'))
        self.assertIsNone(extract_handoff('```text\nDraft\n```\n```text\nFinal\n```'))

    def test_nontrigger_output_has_no_handoff(self):
        self.assertIsNone(extract_handoff('A binary search tree stores sorted keys. Search follows branches.'))

    def test_model_invocation_and_completion_are_observed(self):
        events = [
            {'type': 'assistant', 'message': {'model': 'observed-model', 'content': [
                {'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'promptcraft:promptcraft'}}]}},
            {'type': 'result', 'result': '```text\nFix Save.\n```', 'is_error': False,
             'usage': {'input_tokens': 12, 'output_tokens': 5}},
        ]
        parsed = parse_events('\n'.join(json.dumps(row) for row in events))
        self.assertEqual(parsed['skill_calls'], ['promptcraft:promptcraft'])
        self.assertEqual(parsed['models_observed'], ['observed-model'])
        self.assertEqual(parsed['handoff_chars'], 9)
        self.assertEqual(parsed['status'], 'RUN')

    def test_error_or_missing_result_is_not_success(self):
        self.assertEqual(parse_events('')['status'], 'ERROR')
        self.assertEqual(parse_events(json.dumps({'type': 'result', 'result': 'partial', 'is_error': True}))['status'], 'ERROR')


if __name__ == '__main__':
    unittest.main()
