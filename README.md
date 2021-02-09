# TCC: Privacidade de Dados em *Smart Contracts*
Esse repositório provê a evolução da implementação da prova de conceito do artigo "*Smart Contracts* como uma plataforma para computação segura", o qual foi escrito por Ivan da Silva Sendin (@ivansendin) e Bianca Cristina da Silva (@BiancaCristina) e submetido ao Simpósio Brasileiro em Segurança da Informação e de Sistemas Computacionais (SBSeg) 2020. O repositório específico do artigo está disponível [aqui](https://github.com/BiancaCristina/Artigo-SC).

Na evolução do artigo, quesitos de segurança tais como o *commit* das permutações foram implementados bem como a melhora da documentação geral da biblioteca. Além disso, a evolução é direcionada ao Trabalho de Conclusão de Curso (TCC) de Bianca Cristina da Silva (@BiancaCristina).

## Visão Geral
A implementação consiste usufrui de *smart contracts* a fim de possibilitar a execução de computações de tabelas-verdade entre múltiplas entidades. Para tal, a ferramenta Brownie (documentação disponível [aqui](https://eth-brownie.readthedocs.io/en/stable/)), framework que permite o desenvolvimento e teste de *smart contracts* por meio da simulação da *Ethereum Virtual Machine (EVM)*. 

## Instalação
### Pré requisitos
É necessário instalar o Brownie e Ganache para, futuramente, conseguir executar o projeto. Siga [esse tutorial](https://medium.com/better-programming/part-1-brownie-smart-contracts-framework-for-ethereum-basics-5efc80205413) para instalar tais ferramentas. 

### Projeto
Para instalar o projeto localmente basta realizar o clone do repositório.

**Via HTTP**:
```
git clone https://github.com/BiancaCristina/Artigo-SC.git
```

**Via SSH**:
```
git clone git@github.com:BiancaCristina/Artigo-SC.git
```

## Execução
### (1) Ganache
Para iniciar o Ganache, basta:  
```bash
./${DIRETORIO_GANACHE}/ganache
```

### (2) Brownie
Para criar uma rede no Brownie, o comando base abaixo pode ser utilizado:
```bash
brownie networks add ${CATEGORIA_REDE} ${NOME_REDE} host=${HOST} cmd=${GANACHE}
```

Um exemplo de como executar o comando base para criação da rede é dado por:
```bash
brownie networks add Development smc host=http://127.0.0.1:7545 cmd=ganache-cli
```

Uma vez criada a rede, basta executar o comando que abre o console do Brownie da seguinte forma:
```bash
brownie compile
brownie console --network smc
```

Finalmente, rode o script de exemplo disponibilizado no repositório:
```python
run('execution-example')
```

## Testes
Para rodar os testes unitário, basta:
```bash
brownie test --network smc
```