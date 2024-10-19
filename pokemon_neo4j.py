import scrapy
from scrapy.exceptions import CloseSpider
from neo4j import GraphDatabase

class PokemonScrapper(scrapy.Spider):
    name = 'pokemon_neo4j'
    start_urls = ["https://pokemondb.net/pokedex/all"]

    def __init__(self, *args, **kwargs):
        super(PokemonScrapper, self).__init__(*args, **kwargs)
        try:
            self.driver = GraphDatabase.driver("neo4j+s://ab619410.databases.neo4j.io", auth=("neo4j", "y9zQkjdclFk6q9zqKLUCfyRFFcJVcmZJQUr73QPTcaI"))
            self.logger.info("Conexão com o Neo4j estabelecida.")
        except Exception as e:
            self.logger.error(f"Erro ao conectar ao Neo4j: {e}")

    def parse(self, response):
        pokemons = response.css('#pokedex > tbody > tr')
        for pokemon in pokemons:
            link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
            yield response.follow(link, self.parse_pokemon)

    def parse_pokemon(self, response):
        pokemon_name = response.css('#main > h1::text').get()
        pokedex_number = response.css('.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get()

        weight_info = response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get()
        height_info = response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get()

        # Tratando dados nulos
        if not weight_info or not height_info:
            self.logger.error(f"Weight or height info is missing for {pokemon_name}.")
            raise CloseSpider("Missing weight or height info.")

        # Processando o peso
        weight_parts = weight_info.split()
        if len(weight_parts) >= 2:
            weight_value = weight_parts[0]
            weight_unit = weight_parts[1]
        else:
            weight_value = weight_info
            weight_unit = ''  # Defina a unidade como vazia se não puder separar

        # Processando a altura
        height_value = height_info.split(' ')[0].replace('m', '') if height_info else ""

        # Habilidades
        abilities_info = response.css('.data-table > tbody > tr:nth-child(1) > td:nth-child(2) > a::text').getall()

        # Capturando o tipo do Pokémon
        pokemon_type = response.css('.vitals-table > tbody > tr:nth-child(2) > td > a::text').get()

        # Capturando a evolução
        next_evolution = []
        next_evolution_info = response.css('.evolutions > tbody > tr')  # Ajuste o seletor conforme a estrutura do HTML
        for evo in next_evolution_info:
            evo_number = evo.xpath('span[contains(@class, "infocard-lg-data")]/small/text()').get()
            evo_name = evo.xpath('span[contains(@class, "infocard-lg-data")]/a[contains(@class, "ent-name")]/text()').get()
            evo_url = evo.xpath('span[contains(@class, "infocard-lg-data")]/a[contains(@class, "ent-name")]/@href').get()

            if evo_number and evo_name and evo_url:
                evolution = f"#{evo_number} - {evo_name} ({response.urljoin(evo_url)})"
                next_evolution.append(evolution)

        self.logger.info(f"Nome: {pokemon_name}, Pokedex: {pokedex_number}, Peso: {weight_value} {weight_unit}, Altura: {height_value}, Habilidades: {abilities_info}, Tipo: {pokemon_type}, Evoluções: {next_evolution}")
    
        # Inserindo dados no Neo4j
        try:
            with self.driver.session() as session:
                session.write_transaction(self.create_pokemon_node, pokedex_number, pokemon_name, weight_value, weight_unit, height_value, abilities_info, pokemon_type, next_evolution)
                self.logger.info(f"{pokemon_name} inserido no Neo4j com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao inserir {pokemon_name} no Neo4j: {e}")

    def insert_pokemon_data(self, pokedex_number, pokemon_name, weight_value, weight_unit, height_value, abilities, pokemon_type, evo_number, evo_name):
        try:
            with self.driver.session() as session:
                session.write_transaction(self.create_pokemon_node, pokedex_number, pokemon_name, weight_value, weight_unit, height_value, abilities, pokemon_type)
                # Criar a relação de evolução
                session.write_transaction(self.create_evolution_relationship, pokemon_name, evo_number, evo_name)
                self.logger.info(f"{pokemon_name} inserido no Neo4j com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao inserir {pokemon_name} no Neo4j: {e}")

    @staticmethod
    def create_pokemon_node(tx, pokedex_number, pokemon_name, weight_value, weight_unit, height_value, abilities, pokemon_type, evolutions):
        tx.run(
            "CREATE (p:Pokemon {pokedex_number: $pokedex_number, name: $name, weight: $weight, weight_unit: $weight_unit, height: $height, abilities: $abilities, type: $type, evolution: $evolution})",
            pokedex_number=pokedex_number,
            name=pokemon_name,
            weight=weight_value,
            weight_unit=weight_unit,
            height=height_value,
            abilities=abilities,
            type=pokemon_type,
            evolution=evolutions
        )

    @staticmethod
    def create_evolution_relationship(tx, pokemon_name, evo_number, evo_name):
        tx.run(
            """
            MATCH (p:Pokemon {name: $pokemon_name}), (e:Pokemon {name: $evo_name})
            CREATE (p)-[:EVOLVES_TO]->(e)
            """,
            pokemon_name=pokemon_name,
            evo_name=evo_name
        )
    @staticmethod
    def create_ice_colors(tx,pokemon_name, pokemon_type):
        tx.run(
            """
            MATCH (p:Pokemon)
            WHERE p.type = "Ice"
            RETURN COUNT(p) AS ice_pokemon_count;
            """,
            pokemon_name = pokemon_name,
            pokemon_type = pokemon_type
        )

    def closed(self, reason):
        self.driver.close()
