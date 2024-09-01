import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('pokemons.csv')

#limpagem de dados e conversao
df_cleaned = df.dropna(subset=['pokemon_height', 'pokemon_weight'])
df_cleaned.loc[:, 'pokemon_height'] = df_cleaned['pokemon_height'].str.replace(' cm', '').astype(float)
df_cleaned.loc[:, 'pokemon_weight'] = df_cleaned['pokemon_weight'].str.replace(' kg', '').astype(float)

print("Primeiras linhas do DataFrame tratado:")
print(df_cleaned.head())

# top 5 pesados
top_pesados = df_cleaned.sort_values(by='pokemon_weight', ascending=False).head(5)
print("\nTop 5 Pokémons mais pesados:")
print(top_pesados[['pokedex_number', 'pokemon_name', 'pokemon_weight', 'pokemon_height', 'pokemon_type']])

# top 5 altos
top_altos = df_cleaned.sort_values(by='pokemon_height', ascending=False).head(5)
print("\nTop 5 Pokémons mais altos:")
print(top_altos[['pokedex_number', 'pokemon_name', 'pokemon_weight', 'pokemon_height', 'pokemon_type']])

# contagem de Pokémons por tipo
tipo_counts = df_cleaned['pokemon_type'].value_counts()
tipo_counts_df = tipo_counts.reset_index()
tipo_counts_df.columns = ['pokemon_type', 'count']
print("\nContagem de Pokémons por tipo:")
print(tipo_counts_df)

## Gráficos ##

# gráfico dos 5 mais pesados
plt.figure(figsize=(10, 6))
plt.bar(top_pesados['pokemon_name'], top_pesados['pokemon_weight'], color='orange')
plt.xlabel('Pokémon')
plt.ylabel('Peso (kg)')
plt.title('Top 5 Pokémon Mais Pesados')
plt.show()

# gráfico dos 5 mais altos
plt.figure(figsize=(10, 6))
plt.bar(top_altos['pokemon_name'], top_altos['pokemon_height'], color='green')
plt.xlabel('Pokémon')
plt.ylabel('Altura (cm)')
plt.title('Top 5 Pokémon Mais Altos')
plt.show()

# gráfico para a contagem dos tipos de Pokémon
plt.figure(figsize=(10, 6))
plt.bar(tipo_counts_df['pokemon_type'], tipo_counts_df['count'], color='blue')
plt.xlabel('Tipo de Pokémon')
plt.ylabel('Quantidade')
plt.title('Contagem de Pokémon por Tipo')
plt.show()
