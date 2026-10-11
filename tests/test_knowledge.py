import copy
import json
import unittest
from pathlib import Path

from scripts.validate import validate_knowledge

ROOT = Path(__file__).resolve().parents[1]


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        folder = ROOT / 'skills/promptcraft/references'
        self.knowledge = json.loads((folder / 'knowledge.json').read_text())
        self.registry = json.loads((folder / 'sources.json').read_text())

    def test_curated_recommendations_have_official_scoped_provenance(self):
        validate_knowledge(self.knowledge, self.registry)

    def test_missing_provenance_does_not_become_valid_official_advice(self):
        for field in ['url', 'source_title', 'retrieval_date', 'applicable_model_family',
                      'evidence_or_limitation', 'promptcraft_applicability', 'conflicts_with_existing_guidance']:
            with self.subTest(field=field):
                content = copy.deepcopy(self.knowledge)
                content['recommendations'][0].pop(field)
                with self.assertRaises(ValueError):
                    validate_knowledge(content, self.registry)

    def test_unregistered_or_misattributed_source_is_rejected(self):
        for field, value in [('url', 'https://untrusted.example/instructions'), ('provider', 'anthropic')]:
            content = copy.deepcopy(self.knowledge)
            content['recommendations'][0][field] = value
            with self.assertRaises(ValueError):
                validate_knowledge(content, self.registry)

    def test_a_provider_technique_cannot_become_a_universal_requirement(self):
        content = copy.deepcopy(self.knowledge)
        content['recommendations'][0]['mandatory_for_all_prompts'] = True
        with self.assertRaises(ValueError):
            validate_knowledge(content, self.registry)

    def test_unknown_evidence_label_is_rejected(self):
        content = copy.deepcopy(self.knowledge)
        content['recommendations'][0]['labels'] = ['OFFICIAL', 'PROVEN']
        with self.assertRaises(ValueError):
            validate_knowledge(content, self.registry)
