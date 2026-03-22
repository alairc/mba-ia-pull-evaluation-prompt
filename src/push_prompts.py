"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt no Hub (ex: "meu_user/bug_to_user_story_v2")
        prompt_data: Dados do prompt carregados do YAML

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "{bug_report}")

        # Criar ChatPromptTemplate com system e user messages
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt),
        ])

        print(f"   Fazendo push do prompt: {prompt_name}")
        hub.push(prompt_name, prompt_template, new_repo_is_public=True)
        print(f"   ✓ Prompt publicado com sucesso (público)")

        return True

    except Exception as e:
        print(f"  Erro ao fazer push: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    # Verificar campos obrigatórios
    if not prompt_data.get("system_prompt", "").strip():
        errors.append("system_prompt está vazio")

    if not prompt_data.get("user_prompt", "").strip():
        errors.append("user_prompt está vazio")

    if not prompt_data.get("description", "").strip():
        errors.append("description está vazio")

    # Verificar técnicas aplicadas
    techniques = prompt_data.get("techniques_applied", [])
    if len(techniques) < 2:
        errors.append(f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}")

    # Verificar TODOs remanescentes
    system_prompt = prompt_data.get("system_prompt", "")
    if "[TODO]" in system_prompt or "TODO" in system_prompt:
        errors.append("system_prompt ainda contém TODOs")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS AO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")

    # Carregar prompt otimizado
    yaml_path = "prompts/bug_to_user_story_v2.yml"
    data = load_yaml(yaml_path)

    if data is None:
        print(f"\n Não foi possível carregar: {yaml_path}")
        return 1

    prompt_data = data.get("bug_to_user_story_v2")
    if prompt_data is None:
        print("\n Chave 'bug_to_user_story_v2' não encontrada no YAML")
        return 1

    # Validar prompt
    print("\n🔍 Validando prompt...")
    is_valid, errors = validate_prompt(prompt_data)

    if not is_valid:
        print("   Prompt inválido:")
        for err in errors:
            print(f"      - {err}")
        return 1

    print("   ✓ Prompt válido!")

    # Push para o LangSmith Hub
    prompt_name = f"{username}/bug_to_user_story_v2"
    print(f"\n Enviando para o LangSmith Hub...")

    if push_prompt_to_langsmith(prompt_name, prompt_data):
        print(f"\n Push concluído com sucesso!")
        print(f"   Prompt disponível em: https://smith.langchain.com/hub/{prompt_name}")
        return 0
    else:
        print(f"\n Falha ao fazer push do prompt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
