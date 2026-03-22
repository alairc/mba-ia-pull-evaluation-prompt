"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@pytest.fixture
def prompt_data():
    """Fixture que carrega os dados do prompt v2."""
    data = load_prompts(PROMPT_FILE)
    return data["bug_to_user_story_v2"]


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt_data, "Campo 'system_prompt' não encontrado no YAML"
        assert prompt_data["system_prompt"].strip(), "Campo 'system_prompt' está vazio"

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        system_prompt = prompt_data["system_prompt"].lower()
        role_keywords = ["você é um", "você é uma", "atue como", "seu papel é", "product manager"]
        assert any(kw in system_prompt for kw in role_keywords), (
            "O prompt não define uma persona/role. "
            "Inclua algo como 'Você é um Product Manager' no system_prompt."
        )

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt_data["system_prompt"].lower()
        format_keywords = ["markdown", "user story", "como um", "eu quero", "para que", "formato"]
        assert any(kw in system_prompt for kw in format_keywords), (
            "O prompt não menciona formato de saída. "
            "Inclua instruções sobre formato Markdown ou User Story."
        )

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data["system_prompt"].lower()
        example_keywords = ["exemplo", "example", "entrada", "saída", "bug report", "user story gerada"]
        has_examples = sum(1 for kw in example_keywords if kw in system_prompt) >= 2
        assert has_examples, (
            "O prompt não contém exemplos Few-shot suficientes. "
            "Inclua pelo menos um exemplo completo de entrada (bug) e saída (user story)."
        )

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum [TODO] no texto."""
        full_text = yaml.dump(prompt_data, allow_unicode=True)
        assert "[TODO]" not in full_text, "Ainda existem [TODO] no prompt. Remova todos antes de entregar."
        assert "[PENDENTE]" not in full_text, "Ainda existem [PENDENTE] no prompt."

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt_data.get("techniques_applied", [])
        assert len(techniques) >= 2, (
            f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}. "
            f"Adicione o campo 'techniques_applied' com pelo menos 2 técnicas."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
