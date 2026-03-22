"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml


SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt do LangSmith Hub e retorna os dados extraídos.

    Returns:
        dict com os dados do prompt ou None se erro
    """
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    print(f"   Puxando prompt: {prompt_name}")

    try:
        prompt = hub.pull(prompt_name)
        print(f"   ✓ Prompt carregado com sucesso do Hub")

        # Extrair mensagens do ChatPromptTemplate
        system_prompt = ""
        user_prompt = ""

        for msg in prompt.messages:
            msg_type = msg.__class__.__name__
            content = msg.prompt.template if hasattr(msg, 'prompt') else str(msg.content)

            if "System" in msg_type:
                system_prompt = content
            elif "Human" in msg_type:
                user_prompt = content

        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "version": "v1",
                "created_at": "2025-01-15",
                "tags": ["bug-analysis", "user-story", "product-management"],
            }
        }

        return prompt_data

    except Exception as e:
        print(f"   ❌ Erro ao fazer pull do prompt: {e}")
        return None


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    prompt_data = pull_prompts_from_langsmith()

    if prompt_data is None:
        print("\n Falha ao fazer pull dos prompts")
        return 1

    # Salvar em arquivo YAML
    output_path = "prompts/bug_to_user_story_v1.yml"
    if save_yaml(prompt_data, output_path):
        print(f"\n   Prompt salvo em: {output_path}")
    else:
        print(f"\n   Erro ao salvar prompt em: {output_path}")
        return 1

    print("\n Pull concluído com sucesso!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
