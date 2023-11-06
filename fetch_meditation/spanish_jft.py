from typing import Dict, List, Any
import pytz
from datetime import datetime
from bs4 import BeautifulSoup
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.jft_entry import JftEntry


class SpanishJft:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> 'JftEntry':
        timezone = pytz.timezone('America/Mexico_City')
        date = datetime.now(timezone)
        url = 'https://forozonalatino.org/wp-content/uploads/meditaciones/' + date.strftime('%m/%d') + '.html'
        data = HttpUtility.http_get(url)
        soup = BeautifulSoup(data, 'html.parser')

        # Get content
        paragraphs = []
        for i in range(1, 4):
            comment = soup.find(string=f'PARRAFO {i}')
            if comment:
                paragraph = comment.find_next('p').get_text(strip=True)
                paragraphs.append(paragraph)

        # Get Thought
        start_comment = soup.find(string='SOLO X HOY insertar AQUI sin el Solo por Hoy')
        end_comment = soup.find(string='FIN SOLO X HOY')

        extracted_thought = ''
        if start_comment and end_comment:
            start_node = start_comment.find_next_sibling()
            while start_node and start_node != end_comment:
                extracted_thought += str(start_node)
                start_node = start_node.find_next_sibling()

        result = {}
        for element in soup.find_all('p'):
            class_name = element.get('class', [])
            if class_name == ['fecha-sxh']:
                result['date'] = element.get_text()
            elif class_name == ['titulo-sxh']:
                result['title'] = element.get_text()
            elif class_name == ['descripcion-sxh']:
                result['quote'] = element.get_text(strip=True)
            elif class_name == ['numero-pagina-sxh']:
                result['source'] = element.get_text()
            elif class_name == ['soloxhoycontainer']:
                result['thought'] = element.get_text()

        result['content'] = paragraphs
        result['page'] = ''
        result[
            'copyright'] = 'Servicio del Foro Zonal Latinoamericano, Copyright 2017 NA World Services, Inc. Todos los Derechos Reservados.'
        result['thought'] = 'Sólo por Hoy: ' + extracted_thought.strip()

        return JftEntry(
            result['date'],
            result['title'],
            result['page'],
            result['quote'],
            result['source'],
            result['content'],
            result['thought'],
            result['copyright']
        )
