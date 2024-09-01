## Para gerar o csv entre no arquivo pokemon_scrapper.py cole no terminal

```python -m scrapy runspider pokemon_scrapper.py```

## Para apenas gerar o tratamento e os graficos apenas debug o arquivo tratamento.py (Crtl + F5)

# Objetivo

O objetivo deste trabalho foi realizar uma análise detalhada dos dados de Pokémon coletados através de web scraping. O foco foi na extração e limpeza dos dados, seguido por uma análise exploratória utilizando a biblioteca Pandas e visualização gráfica com Matplotlib.

# Coleta de Dados

## Os dados foram coletados do site Pokémon Database utilizando o framework Scrapy. As informações coletadas incluíram:

- Número da Pokédex
- Nome do Pokémon
- Próxima evolução
- Peso
- Altura
- Tipo
- Habilidades

## Processamento e Limpeza dos Dados

Após a coleta, os dados foram armazenados em um arquivo CSV e carregados em um DataFrame do Pandas. As etapas de limpeza incluíram:

### Remoção de Valores Nulos: Linhas com dados faltantes para altura ou peso foram removidas.

### Conversão de Tipos: 

A altura e o peso foram convertidos de strings com unidades ("cm" e "kg") para valores numéricos para facilitar a análise.

## Análise dos Dados

- **Top 5 Pokémons Mais Pesados:**
        Ordenação dos Pokémons por peso e seleção dos cinco mais pesados.
        Exibição dos dados, incluindo número da Pokédex, nome, peso, altura e tipo.

- **Top 5 Pokémons Mais Altos:**
        Ordenação dos Pokémons por altura e seleção dos cinco mais altos.
        Exibição dos dados, incluindo número da Pokédex, nome, peso, altura e tipo.

- **Contagem de Pokémons por Tipo:**
        Cálculo e exibição da quantidade de Pokémons para cada tipo.

## Visualização dos Dados

- Gráficos foram gerados para melhor compreensão dos dados:

- **Gráfico dos 5 Pokémons Mais Pesados:**
        Um gráfico de barras mostrando o peso dos cinco Pokémons mais pesados.

- **Gráfico dos 5 Pokémons Mais Altos:**
        Um gráfico de barras mostrando a altura dos cinco Pokémons mais altos.

- **Contagem de Tipos de Pokémon:**
        Um gráfico de barras mostrando a distribuição dos Pokémons por tipo.