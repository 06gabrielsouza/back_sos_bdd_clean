# Back-S.O.S - Testes BDD

Testes automatizados em Behavior-Driven Development para o sistema de denúncias anônimas Back-S.O.S.

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone <(https://github.com/06gabrielsouza/back_sos_bdd_clean)>
cd back_sos_bdd
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-bdd.txt
```

## Executar os Testes

```bash
behave features/
```

Para saída mais detalhada:

```bash
behave features/ -v
```

## Estrutura do Projeto

```
features/
├── cadastro_denuncia.feature      # Cenários de teste em Gherkin
├── environment.py                  # Setup e hooks do Behave
└── steps/
    ├── __init__.py
    ├── helpers.py                  # Cliente API e validadores
    └── cadastro_denuncia_steps.py  # Implementação dos testes
```

## Cenários Testados

- ✅ Criar denúncia com todos os campos
- ✅ Validar campo título obrigatório
- ✅ Validar campo descrição obrigatório
- ✅ Validar tipo de denúncia obrigatório
- ✅ Garantir anonimato da denúncia
- ✅ Exigir autenticação para acessar

## Resultados

```
1 feature passed
6 scenarios passed
50 steps passed
0 failed
```

## Próximos Passos

- Integrar com a API real do Back-S.O.S
- Adicionar testes de UI com Selenium
- Configurar CI/CD (GitHub Actions)

## Documentação

Veja os arquivos markdown para mais detalhes:
- `GUIA_BDD.md` - Documentação completa
- `INSTRUCOES.md` - Passo a passo
- `RESUMO_TESTES.md` - Resultados dos testes
