# language: pt
Funcionalidade: Cadastro de Denúncia Confidencial
  Como um aluno ou responsável
  Eu quero poder registrar uma denúncia de forma anônima e confidencial
  Para que a equipe pedagógica possa investigar e resolver problemas na escola

  Cenário: Aluno abre uma denúncia com sucesso preenchendo todos os campos obrigatórios
    Dado que o usuário está autenticado no sistema
    E ele acessa a página de "Nova Denúncia"
    Quando ele preenche o título com "Bullying na sala de aula"
    E ele preenche a descrição com "Um colega está me intimidando durante as aulas"
    E ele seleciona o tipo de denúncia "Bullying"
    E ele seleciona a localização "Sala 101"
    E ele clica no botão "Enviar Denúncia"
    Então o sistema deve registrar a denúncia com status "Aberta"
    E um protocolo de denúncia deve ser gerado
    E o usuário deve receber uma mensagem de sucesso com o número do protocolo
    E o usuário deve ser redirecionado para a página de confirmação

  Cenário: Tentativa de abrir denúncia sem preencher o título
    Dado que o usuário está autenticado no sistema
    E ele acessa a página de "Nova Denúncia"
    Quando ele preenche a descrição com "Problema na cantina"
    E ele seleciona o tipo de denúncia "Infraestrutura"
    E ele seleciona a localização "Cantina"
    E ele clica no botão "Enviar Denúncia"
    Então o sistema não deve registrar a denúncia
    E uma mensagem de erro "O campo título é obrigatório." deve ser exibida
    E o usuário deve permanecer na página de criação de denúncia

  Cenário: Tentativa de abrir denúncia sem preencher a descrição
    Dado que o usuário está autenticado no sistema
    E ele acessa a página de "Nova Denúncia"
    Quando ele preenche o título com "Problema com professor"
    E ele seleciona o tipo de denúncia "Assédio"
    E ele seleciona a localização "Sala 102"
    E ele clica no botão "Enviar Denúncia"
    Então o sistema não deve registrar a denúncia
    E uma mensagem de erro "O campo descrição é obrigatório." deve ser exibida

  Cenário: Tentativa de abrir denúncia sem selecionar o tipo
    Dado que o usuário está autenticado no sistema
    E ele acessa a página de "Nova Denúncia"
    Quando ele preenche o título com "Violência na escola"
    E ele preenche a descrição com "Presenciei um ato de violência"
    E ele seleciona a localização "Pátio"
    E ele clica no botão "Enviar Denúncia"
    Então o sistema não deve registrar a denúncia
    E uma mensagem de erro "Selecione um tipo de denúncia." deve ser exibida

  Cenário: Denúncia é criada com anonimato garantido
    Dado que o usuário está autenticado no sistema
    E ele acessa a página de "Nova Denúncia"
    Quando ele preenche o título com "Problema na biblioteca"
    E ele preenche a descrição com "Falta de livros na biblioteca"
    E ele seleciona o tipo de denúncia "Infraestrutura"
    E ele seleciona a localização "Biblioteca"
    E ele clica no botão "Enviar Denúncia"
    Então o sistema deve registrar a denúncia com status "Aberta"
    E a denúncia não deve conter informações pessoais identificáveis do denunciante
    E apenas o protocolo deve ser associado à denúncia para rastreamento

  Cenário: Usuário não autenticado tenta acessar a página de nova denúncia
    Dado que o usuário não está autenticado no sistema
    Quando ele tenta acessar a página de "Nova Denúncia"
    Então ele deve ser redirecionado para a página de login
    E uma mensagem "Você precisa estar autenticado para fazer uma denúncia." deve ser exibida
