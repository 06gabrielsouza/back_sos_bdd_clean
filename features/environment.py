"""
Arquivo de configuração do Behave para o projeto Back-S.O.S BDD.
Define hooks e configurações globais para os testes.
"""

import os
import sys
from datetime import datetime

# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def before_all(context):
    """Executado uma vez antes de todos os testes."""
    print("\n" + "="*70)
    print("Iniciando testes BDD - Back-S.O.S")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*70 + "\n")
    
    # Inicializar contexto global
    context.base_url = os.getenv("API_BASE_URL", "http://localhost:8080")
    context.test_user = None
    context.created_denuncia = None
    context.protocol_number = None
    context.error_message = None
    context.response = None


def before_scenario(context, scenario):
    """Executado antes de cada cenário."""
    print(f"\n▶ Cenário: {scenario.name}")
    context.test_user = None
    context.created_denuncia = None
    context.protocol_number = None
    context.error_message = None
    context.response = None


def after_scenario(context, scenario):
    """Executado após cada cenário."""
    status = "✓ PASSOU" if scenario.status == "passed" else "✗ FALHOU"
    print(f"  {status}\n")


def after_all(context):
    """Executado uma vez após todos os testes."""
    print("\n" + "="*70)
    print("Testes BDD concluídos")
    print("="*70 + "\n")
