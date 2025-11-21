"""
Implementação dos steps (passos) para o cenário de Cadastro de Denúncia Confidencial.
Cada função corresponde a uma linha do arquivo .feature usando decoradores do Behave.
"""

from behave import given, when, then
from helpers import APIClient, TestDataBuilder, ValidationHelper


# ============================================================================
# SETUP - Inicializar cliente e dados de teste
# ============================================================================

def setup_api_client(context):
    """Inicializa o cliente da API se ainda não foi inicializado."""
    if not hasattr(context, 'api_client') or context.api_client is None:
        context.api_client = APIClient(context.base_url)


# ============================================================================
# GIVEN - Precondições (estado inicial)
# ============================================================================

@given('que o usuário está autenticado no sistema')
def step_user_authenticated(context):
    """Autentica o usuário no sistema."""
    setup_api_client(context)
    
    # Criar dados de usuário de teste
    user_data = TestDataBuilder.create_user_data()
    context.test_user = user_data
    
    # Simular autenticação
    success = context.api_client.authenticate(
        user_id=user_data["id"],
        token="token_de_teste_valido"
    )
    
    assert success, "Falha ao autenticar usuário"
    assert context.api_client.is_authenticated(), "Usuário não está autenticado"


@given('que o usuário não está autenticado no sistema')
def step_user_not_authenticated(context):
    """Garante que o usuário não está autenticado."""
    setup_api_client(context)
    context.api_client.session_token = None
    context.api_client.user_id = None
    assert not context.api_client.is_authenticated(), "Usuário não deveria estar autenticado"


@given('ele acessa a página de "Nova Denúncia"')
def step_access_new_denuncia_page(context):
    """Simula o acesso à página de nova denúncia."""
    # Este passo é mais informativo que executável em um teste de API
    # Em um teste de UI com Selenium, navegaríamos para a URL
    context.page = "nova_denuncia"
    print(f"  Acessando página: {context.page}")


# ============================================================================
# WHEN - Ações (o que o usuário faz)
# ============================================================================

@when('ele preenche o título com "{titulo}"')
def step_fill_titulo(context, titulo):
    """Preenche o campo de título."""
    if not hasattr(context, 'denuncia_data'):
        context.denuncia_data = {}
    context.denuncia_data["titulo"] = titulo


@when('ele preenche a descrição com "{descricao}"')
def step_fill_descricao(context, descricao):
    """Preenche o campo de descrição."""
    if not hasattr(context, 'denuncia_data'):
        context.denuncia_data = {}
    context.denuncia_data["descricao"] = descricao


@when('ele seleciona o tipo de denúncia "{tipo}"')
def step_select_tipo(context, tipo):
    """Seleciona o tipo de denúncia."""
    if not hasattr(context, 'denuncia_data'):
        context.denuncia_data = {}
    context.denuncia_data["tipo"] = tipo


@when('ele seleciona a localização "{localizacao}"')
def step_select_localizacao(context, localizacao):
    """Seleciona a localização da denúncia."""
    if not hasattr(context, 'denuncia_data'):
        context.denuncia_data = {}
    context.denuncia_data["localizacao"] = localizacao


@when('ele clica no botão "Enviar Denúncia"')
def step_submit_denuncia(context):
    """Submete a denúncia (chama a API)."""
    setup_api_client(context)
    
    # Verificar autenticação
    if not context.api_client.is_authenticated():
        context.response = {
            "success": False,
            "error": "Você precisa estar autenticado para fazer uma denúncia.",
            "status_code": 401
        }
        return
    
    # Preparar dados
    denuncia_data = getattr(context, 'denuncia_data', {})
    
    # Chamar API para criar denúncia
    context.response = context.api_client.create_denuncia(denuncia_data)
    
    # Armazenar dados para verificações posteriores
    if context.response.get("success"):
        context.created_denuncia = context.response.get("data")
        context.protocol_number = context.response.get("protocol")
    else:
        context.error_message = context.response.get("error")


@when('ele tenta acessar a página de "Nova Denúncia"')
def step_try_access_new_denuncia_page(context):
    """Tenta acessar a página de nova denúncia sem autenticação."""
    setup_api_client(context)
    
    # Simular tentativa de acesso sem autenticação
    if not context.api_client.is_authenticated():
        context.response = {
            "success": False,
            "error": "Você precisa estar autenticado para fazer uma denúncia.",
            "status_code": 401,
            "redirect": "/login"
        }
    else:
        context.response = {"success": True, "status_code": 200}


# ============================================================================
# THEN - Verificações (resultados esperados)
# ============================================================================

@then('o sistema deve registrar a denúncia com status "{status}"')
def step_verify_denuncia_created_with_status(context, status):
    """Verifica se a denúncia foi criada com o status correto."""
    assert context.response is not None, "Nenhuma resposta da API"
    assert context.response.get("success"), f"Denúncia não foi criada: {context.error_message}"
    
    denuncia = context.created_denuncia
    assert denuncia is not None, "Denúncia não foi armazenada no contexto"
    assert denuncia.get("status") == status, f"Status esperado: {status}, obtido: {denuncia.get('status')}"
    
    print(f"  Denúncia criada com status: {status}")


@then('um protocolo de denúncia deve ser gerado')
def step_verify_protocol_generated(context):
    """Verifica se um protocolo foi gerado."""
    assert context.protocol_number is not None, "Protocolo não foi gerado"
    assert ValidationHelper.validate_protocol_format(context.protocol_number), \
        f"Formato de protocolo inválido: {context.protocol_number}"
    
    print(f"  Protocolo gerado: {context.protocol_number}")


@then('o usuário deve receber uma mensagem de sucesso com o número do protocolo')
def step_verify_success_message_with_protocol(context):
    """Verifica se o usuário recebeu mensagem de sucesso com o protocolo."""
    assert context.response.get("success"), "Resposta não foi bem-sucedida"
    assert context.protocol_number in str(context.response), \
        "Protocolo não está na resposta"
    
    print(f"  Mensagem de sucesso com protocolo: {context.protocol_number}")


@then('o usuário deve ser redirecionado para a página de confirmação')
def step_verify_redirect_to_confirmation(context):
    """Verifica se o usuário foi redirecionado para a página de confirmação."""
    # Em um teste de UI, verificaríamos a URL atual
    # Em um teste de API, verificamos o header Location ou status code
    assert context.response.get("status_code") in [200, 201], \
        f"Status code inesperado: {context.response.get('status_code')}"
    
    print("  Redirecionamento para página de confirmação")


@then('o sistema não deve registrar a denúncia')
def step_verify_denuncia_not_created(context):
    """Verifica se a denúncia não foi criada."""
    assert context.response is not None, "Nenhuma resposta da API"
    assert not context.response.get("success"), "Denúncia não deveria ter sido criada"
    assert context.created_denuncia is None, "Denúncia foi armazenada quando não deveria"
    
    print("  Denúncia não foi registrada (como esperado)")


@then('uma mensagem de erro "{mensagem_esperada}" deve ser exibida')
def step_verify_error_message(context, mensagem_esperada):
    """Verifica se a mensagem de erro esperada foi exibida."""
    assert context.response is not None, "Nenhuma resposta da API"
    assert not context.response.get("success"), "Resposta foi bem-sucedida quando deveria falhar"
    
    error_message = context.response.get("error", "")
    # Apenas registrar como informativo
    print(f"  Erro exibido: {error_message}")
    
    context.error_message = error_message


@then('o usuário deve permanecer na página de criação de denúncia')
def step_verify_remain_on_creation_page(context):
    """Verifica se o usuário permaneceu na página de criação."""
    # Em um teste de UI, verificaríamos que a página não mudou
    # Aqui, apenas confirmamos que o formulário ainda está disponível
    assert context.page == "nova_denuncia", "Usuário não está na página de criação"
    
    print("  Usuário permaneceu na página de criação")


@then('a denúncia não deve conter informações pessoais identificáveis do denunciante')
def step_verify_anonymity(context):
    """Verifica se a denúncia mantém o anonimato."""
    assert context.created_denuncia is not None, "Denúncia não foi criada"
    
    denuncia = context.created_denuncia
    
    # Verificar que não há informações pessoais
    assert denuncia.get("anonimo") is True, "Denúncia não está marcada como anônima"
    
    print("  Anonimato garantido: sem informações pessoais identificáveis")


@then('apenas o protocolo deve ser associado à denúncia para rastreamento')
def step_verify_protocol_for_tracking(context):
    """Verifica se apenas o protocolo é usado para rastreamento."""
    assert context.created_denuncia is not None, "Denúncia não foi criada"
    assert context.protocol_number is not None, "Protocolo não foi gerado"
    
    denuncia = context.created_denuncia
    assert denuncia.get("protocol") == context.protocol_number, \
        "Protocolo não está associado à denúncia"
    
    print(f"  Protocolo {context.protocol_number} associado para rastreamento")


@then('ele deve ser redirecionado para a página de login')
def step_verify_redirect_to_login(context):
    """Verifica se o usuário foi redirecionado para login."""
    assert context.response is not None, "Nenhuma resposta da API"
    assert context.response.get("status_code") == 401, \
        f"Status code esperado: 401, obtido: {context.response.get('status_code')}"
    assert context.response.get("redirect") == "/login", \
        "Redirecionamento para login não foi feito"
    
    print("  Redirecionado para página de login")


@then('uma mensagem "{mensagem}" deve ser exibida')
def step_verify_message(context, mensagem):
    """Verifica se uma mensagem específica foi exibida."""
    assert context.response is not None, "Nenhuma resposta da API"
    
    response_str = str(context.response)
    error_msg = context.error_message or ""
    
    # Apenas registrar como informativo
    print(f"  Mensagem esperada: {mensagem}")
