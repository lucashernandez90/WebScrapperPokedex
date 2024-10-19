import scrapy
import csv

class PokemonScrapper(scrapy.Spider):
    name = 'pokemon_scrapper'
    domain = "https://pokemondb.net/"
    start_urls = ["https://pokemondb.net/pokedex/all"]

    def __init__(self, *args, **kwargs):
        super(PokemonScrapper, self).__init__(*args, **kwargs)
        self.csv_file = open('pokemon.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['pokedex_number', 'pokemon_name', 'next_evolution', 'pokemon_weight', 'pokemon_height', 'pokemon_type', 'pokemon_abilities'])

    def parse(self, response):
        pokemons = response.css('#pokedex > tbody > tr')
        for pokemon in pokemons:
            link = pokemon.css("td.cell-name > a::attr(href)").extract_first()
            yield response.follow(self.domain + link, self.parse_pokemon)

    def parse_pokemon(self, response):
        # Evolução
        next_evolution_info = response.css('div.infocard-list-evo > div.infocard')
        next_evolution = []
        
        for evo in next_evolution_info:
            evo_number = evo.xpath('span[contains(@class, "infocard-lg-data")]/small/text()').get()
            evo_name = evo.xpath('span[contains(@class, "infocard-lg-data")]/a[contains(@class, "ent-name")]/text()').get()
            evo_url = evo.xpath('span[contains(@class, "infocard-lg-data")]/a[contains(@class, "ent-name")]/@href').get()

            if evo_number and evo_name and evo_url:
                evolution = f"#{evo_number} - {evo_name} ({response.urljoin(evo_url)})"
                next_evolution.append(evolution)

        # Peso
        weight_info = response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get()
        weight_parts = weight_info.split()
        weight_value = weight_parts[0] if len(weight_parts) > 0 else ''
        weight_unit = weight_parts[1] if len(weight_parts) > 1 else ''

        # Altura
        height_info = response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get()
        height_value_m = height_info.split(' ')[0].replace('m', '')
        try:
            height_value_cm = float(height_value_m) * 100
            formatted_height = f"{height_value_cm} cm"
        except ValueError:
            formatted_height = height_info 

        # Habilidades
        abilities_info = []
        abilities = response.css('.data-table > tbody > tr:nth-child(1) > td:nth-child(2) > a')
        
        for ability in abilities:
            ability_name = ability.css('::text').get()
            ability_url = ability.css('::attr(href)').get()
            if ability_name and ability_url:
                ability_info = f"{ability_name} ({response.urljoin(ability_url)})"
                abilities_info.append(ability_info)


        data = {
            'pokedex_number': response.css('.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get(),
            'pokemon_name': response.css('#main > h1::text').get(),
            'next_evolution': ', '.join(next_evolution),
            'pokemon_weight': weight_value + ' ' + weight_unit,
            'pokemon_height': formatted_height,
            'pokemon_type': response.css('.vitals-table > tbody > tr:nth-child(2) > td > a::text').get(),
            'pokemon_abilities': ', '.join(abilities_info)
        }

        # Escreve os dados no arquivo CSV
        self.csv_writer.writerow(data.values())

    def parse_ability(self, response):
        # Captura informações da página da habilidade
        ability_name = response.css('h1::text').get()
        ability_description = response.css('div.grid-col > p::text').get()
        
        if ability_description:
            ability_description = ability_description.strip()

        if hasattr(self, 'abilities_info'):
            self.abilities_info.append(f"{ability_name}: {ability_description}")
        else:
            self.abilities_info = [f"{ability_name}: {ability_description}"]

    def closed(self, reason):

        self.csv_file.close()