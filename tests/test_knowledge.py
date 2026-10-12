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

    def test_agent_skills_standard_is_classified_apart_from_prompting_guidance(self):
        from scripts.freshness import validate_registry
        standards = [s for s in self.registry['sources'] if s['provider'] == 'agentskills']
        self.assertEqual(self.registry['policies']['agentskills']['classification'], 'standard')
        self.assertIn('https://agentskills.io/specification', {s['canonical_url'] for s in standards})
        self.assertTrue(all(s['role'] in ('standard', 'index') for s in standards))
        self.assertTrue(all('not model-specific prompting guidance' in s['applicability'] for s in standards))
        # A standard cannot back a model prompting recommendation.
        content = copy.deepcopy(self.knowledge)
        content['recommendations'][0].update(provider='agentskills', url='https://agentskills.io/specification')
        with self.assertRaises(ValueError):
            validate_knowledge(content, self.registry)
        # Model-developer sources cannot use the standard role, and standards cannot pose as guidance.
        for provider, role in (('openai', 'standard'), ('agentskills', 'guidance')):
            registry = copy.deepcopy(self.registry)
            row = next(s for s in registry['sources'] if s['provider'] == provider and s['role'] != 'index')
            row['role'] = role
            with self.subTest(provider=provider, role=role), self.assertRaises(ValueError):
                validate_registry(registry)
