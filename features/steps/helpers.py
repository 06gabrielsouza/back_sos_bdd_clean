"""
Helpers e utilitários para os testes BDD do Back-S.O.S.
Fornece funções para simular requisições à API e gerenciar dados de teste.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional


class APIClient:
    """Cliente simulado para interagir com a API Back-S.O.S."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session_token = None
        self.user_id = None
        self.denuncias = {}  # Simulação de banco de dados em memória
        
    def authenticate(self, user_id: str, token: str) -> bool:
        """Simula autenticação do usuário."""
        self.user_id = user_id
        self.session_token = token
        return True
    
    def is_authenticated(self) -> bool:
        """Verifica se o usuário está autenticado."""
        return self.session_token is not None
    
    def create_denuncia(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma nova denúncia.
        
        Args:
            data: Dicionário com os dados da denúncia
            
        Returns:
            Dicionário com a resposta da API
        """
        # Validar campos obrigatórios
        required_fields = ["titulo", "descricao", "tipo", "localizacao"]
        for field in required_fields:
            if field not in data or not data[field]:
                return {
                    "success": False,
                    "error": f"O campo {field} é obrigatório.",
                    "status_code": 400
                }
        
        # Gerar protocolo único
        protocol_number = f"SOS-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        
        # Criar denúncia (simulação)
        denuncia = {
            "id": str(uuid.uuid4()),
            "protocol": protocol_number,
            "titulo": data["titulo"],
            "descricao": data["descricao"],
            "tipo": data["tipo"],
            "localizacao": data["localizacao"],
            "status": "Aberta",
            "created_at": datetime.now().isoformat(),
            "user_id": self.user_id,
            "anonimo": True  # Sempre anônimo
        }
        
        # Armazenar denúncia
        self.denuncias[denuncia["id"]] = denuncia
        
        return {
            "success": True,
            "data": denuncia,
            "protocol": protocol_number,
            "status_code": 201
        }
    
    def get_denuncia(self, denuncia_id: str) -> Dict[str, Any]:
        """Recupera uma denúncia pelo ID."""
        if denuncia_id in self.denuncias:
            return {
                "success": True,
                "data": self.denuncias[denuncia_id],
                "status_code": 200
            }
        return {
            "success": False,
            "error": "Denúncia não encontrada",
            "status_code": 404
        }
    
    def list_denuncias(self) -> Dict[str, Any]:
        """Lista todas as denúncias."""
        return {
            "success": True,
            "data": list(self.denuncias.values()),
            "status_code": 200
        }
    
    def reset(self):
        """Reseta o estado do cliente (útil para testes)."""
        self.session_token = None
        self.user_id = None
        self.denuncias = {}


class TestDataBuilder:
    """Construtor de dados de teste."""
    
    @staticmethod
    def create_user_data(user_id: str = None) -> Dict[str, Any]:
        """Cria dados de usuário para teste."""
        return {
            "id": user_id or str(uuid.uuid4()),
            "name": "Usuário Teste",
            "email": "teste@escola.com",
            "role": "student"
        }
    
    @staticmethod
    def create_denuncia_data(
        titulo: str = "Denúncia Teste",
        descricao: str = "Descrição de teste",
        tipo: str = "Bullying",
        localizacao: str = "Sala 101"
    ) -> Dict[str, Any]:
        """Cria dados de denúncia para teste."""
        return {
            "titulo": titulo,
            "descricao": descricao,
            "tipo": tipo,
            "localizacao": localizacao
        }


class ValidationHelper:
    """Helper para validações comuns."""
    
    @staticmethod
    def validate_protocol_format(protocol: str) -> bool:
        """Valida o formato do protocolo de denúncia."""
        # Formato esperado: SOS-YYYYMMDD-XXXXXXXX
        parts = protocol.split("-")
        return len(parts) == 3 and parts[0] == "SOS" and len(parts[2]) == 8
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Valida formato de email."""
        return "@" in email and "." in email.split("@")[1]
    
    @staticmethod
    def is_valid_status(status: str) -> bool:
        """Valida se o status é válido."""
        valid_statuses = ["Aberta", "Em Andamento", "Resolvida", "Fechada"]
        return status in valid_statuses
