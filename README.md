# ExploraALMG

Repositório para exploração inicial dos dados abertos disponibilizados pela Assembleia Legislativa de Minas Gerais (ALMG).

Acesse a versão online: [rodfileto-ufmg.github.io/ExploraALMG/](https://rodfileto-ufmg.github.io/ExploraALMG/)

## Sobre

Este projeto tem como objetivo analisar, tratar e explorar os dados públicos fornecidos pela ALMG, facilitando o acesso e a compreensão das informações legislativas do estado de Minas Gerais.


## Estrutura do Repositório

- **docs/**: Documentação e arquivos para publicação do site.
- **documentos/**: Materiais de apoio e documentação adicional.
- **funcoes/**: Scripts e funções auxiliares para manipulação dos dados.
- **montar_db_legislaturas.py**: Script para montar o banco de dados das legislaturas.
- **montar_db_proposicoes.py**: Script para montar o banco de dados das proposições.
- **script.py** e **teste.py**: Scripts principais e de testes.
- **requirements_linux.txt** e **requirements_windows.txt**: Dependências para execução em diferentes sistemas operacionais.

## Como usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/rodfileto-ufmg/ExploraALMG.git
   ```
2. Instale as dependências:

    ```bash
    # Para Linux
    pip install -r requirements_linux.txt

    # Para Windows
    pip install -r requirements_windows.txt
    ```

3. Execute os scripts montar_db_* para criar a base de dados.

4. Renderize index.qmd na pasta documentos.


## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
