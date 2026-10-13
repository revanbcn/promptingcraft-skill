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

    def test_mixed_language_blocks_do_not_mispair_their_fences(self):
        self.assertIsNone(extract_handoff('```python\nprint(1)\n```\n```text\nFix Save.\n```'))

    def test_malformed_fences_are_not_a_complete_handoff(self):
        for text in ['```text\nFix Save.', '```text\nFix Save.\n```\n```python\nprint(1)',
                     '```text\n```']:
            with self.subTest(text=text):
                self.assertIsNone(extract_handoff(text))

    def test_nontrigger_output_has_no_handoff(self):
        self.assertIsNone(extract_handoff('A binary search tree stores sorted keys. Search follows branches.'))

    def test_model_invocation_and_completion_are_observed(self):
        events = [
            {'type': 'assistant', 'message': {'model': 'observed-model', 'content': [
                {'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'promptingcraft:promptingcraft'}}]}},
            {'type': 'result', 'result': '```text\nFix Save.\n```', 'is_error': False,
             'usage': {'input_tokens': 12, 'output_tokens': 5}},
        ]
        parsed = parse_events('\n'.join(json.dumps(row) for row in events))
        self.assertEqual(parsed['skill_calls'], ['promptingcraft:promptingcraft'])
        self.assertEqual(parsed['models_observed'], ['observed-model'])
        self.assertEqual(parsed['handoff_chars'], 9)
        self.assertEqual(parsed['status'], 'RUN')

    def test_error_or_missing_result_is_not_success(self):
        self.assertEqual(parse_events('')['status'], 'ERROR')
        self.assertEqual(parse_events(json.dumps({'type': 'result', 'result': 'partial', 'is_error': True}))['status'], 'ERROR')

    def test_system_message_string_does_not_abort_completed_trace_collection(self):
        events = [
            {'type': 'system', 'subtype': 'permission_denied', 'message': 'Command not allowed'},
            {'type': 'assistant', 'message': {'model': 'observed-model', 'content': []}},
            {'type': 'result', 'is_error': False, 'result': 'Completed visible result'},
        ]
        result = parse_events('\n'.join(json.dumps(event) for event in events))
        self.assertEqual(result['status'], 'RUN')
        self.assertEqual(result['models_observed'], ['observed-model'])


    def test_no_change_reuses_original_instead_of_missing_handoff(self):
        raw = json.dumps({'type': 'result', 'is_error': False,
            'result': 'The original prompt is already suitable.\nNo material revision is necessary.'})
        result = parse_events(raw, original='Fix Save. Do not deploy.')
        self.assertEqual(result['composition_outcome'], 'UNCHANGED')
        self.assertEqual(result['handoff'], 'Fix Save. Do not deploy.')

    def test_no_change_claim_with_rewritten_block_is_unresolved(self):
        raw = json.dumps({'type': 'result', 'is_error': False,
            'result': 'The original prompt is already suitable. No material revision is necessary.\n```text\nDeploy it.\n```'})
        result = parse_events(raw, original='Do not deploy.')
        self.assertEqual(result['composition_outcome'], 'UNRESOLVED')
        self.assertIsNone(result['handoff'])

    def test_no_change_can_echo_the_exact_original_in_a_single_block(self):
        original = 'Fix Save. Do not deploy.'
        raw = json.dumps({'type': 'result', 'is_error': False,
            'result': 'The original prompt is already suitable. No material revision is necessary.\n```text\nFix Save. Do not deploy.\n```'})
        result = parse_events(raw, original=original)
        self.assertEqual(result['composition_outcome'], 'UNCHANGED')
        self.assertEqual(result['handoff'], original)

    def test_rejected_no_change_phrase_is_not_an_outcome(self):
        text = 'Do not use the no-change response "The original prompt is already suitable. No material revision is necessary." here: the deployment clauses conflict. Ask the owner to resolve them.'
        result = parse_events(json.dumps({'type':'result','is_error':False,'result':text}), original='Deployment is forbidden. Deploy immediately.')
        self.assertEqual(result['composition_outcome'], 'UNRESOLVED')
        self.assertIsNone(result['handoff'])

    def test_unchanged_echo_preserves_meaningful_whitespace(self):
        marker = 'The original prompt is already suitable. No material revision is necessary.'
        for original, echoed, expected in [('Fix Save.', '  Fix Save.', 'UNRESOLVED'),
                                           ('  Fix Save.', '  Fix Save.', 'UNCHANGED')]:
            raw = json.dumps({'type':'result','is_error':False,'result':marker+'\n\n```text\n'+echoed+'\n```'})
            result = parse_events(raw, original=original)
            self.assertEqual(result['composition_outcome'], expected)
            if expected == 'UNCHANGED': self.assertEqual(result['handoff'], original)

if __name__ == '__main__':
    unittest.main()
