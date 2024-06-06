# Sistema de Login e Cadastro

Este projeto é um sistema de login e cadastro de usuários desenvolvido em Python, utilizando as bibliotecas `customtkinter` para a interface gráfica e `sqlite3` para o banco de dados.

## Funcionalidades

- **Conectar ao Banco de Dados**: Conecta ao banco de dados SQLite para realizar operações de inserção, atualização e consulta.
- **Criar Tabela**: Cria a tabela `Usuarios` no banco de dados se ela ainda não existir.
- **Cadastrar Usuário**: Permite que novos usuários se cadastrem no sistema, armazenando seu nome de usuário, email, senha e confirmação de senha.
- **Verificar Login**: Verifica as credenciais fornecidas pelos usuários e permite o acesso se os dados estiverem corretos.
- **Interface Gráfica**: Interface de usuário amigável para login e cadastro utilizando a biblioteca `customtkinter`.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-de-login.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd sistema-de-login
   ```
3. Instale as dependências necessárias:
   ```bash
   pip install customtkinter
   ```

## Como Usar

1. Execute o arquivo principal:
   ```bash
   python app.py
   ```
2. **Tela de Login**: Ao iniciar o aplicativo, você verá a tela de login. Se você já tiver uma conta, insira seu nome de usuário e senha para fazer login.
3. **Tela de Cadastro**: Se você não tiver uma conta, clique no botão "Fazer Cadastro" para ir para a tela de cadastro. Preencha todos os campos e clique em "Fazer cadastro" para criar uma nova conta.

## Estrutura do Projeto

### Classe `BackEnd`

Responsável pela interação com o banco de dados.

- `conecta_db()`: Conecta ao banco de dados SQLite.
- `desconecta_db()`: Desconecta do banco de dados.
- `cria_tabela()`: Cria a tabela `Usuarios` no banco de dados.
- `cadastrar_usuario()`: Captura os dados de cadastro do usuário, valida-os e insere um novo registro na tabela `Usuarios`.
- `verifica_login()`: Captura os dados de login do usuário, verifica-os no banco de dados e exibe mensagens de erro ou sucesso.

### Classe `App`

Herda de `ctk.CTk` e `BackEnd`, gerenciando a interface gráfica e chamando métodos de `BackEnd` para manipular dados.

- `__init__()`: Inicializa a janela principal, configura a tela de login e cria a tabela de usuários.
- `configuracoes_da_janela_inicial()`: Configura a aparência inicial da janela principal.
- `tela_de_login()`: Configura e exibe a tela de login.
- `tela_de_cadastro()`: Configura e exibe a tela de cadastro.
- `limpa_entry_cadastro()`: Limpa os campos de entrada da tela de cadastro.
- `limpa_entry_login()`: Limpa os campos de entrada da tela de login.

## Contribuição

1. Fork o repositório.
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b minha-feature
   ```
3. Commit suas mudanças:
   ```bash
   git commit -m 'Minha nova feature'
   ```
4. Push para a branch:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a minha licença. Veja o arquivo para mais detalhes.

---

### Contato

Se você tiver alguma dúvida ou sugestão, sinta-se à vontade para entrar em contato:

- **Email**: lucas12020910@gmail.com

---

Espero que este README forneça uma visão clara do funcionamento e da utilização do sistema de login e cadastro. Se precisar de mais informações, não hesite em perguntar!
 
