import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from pdb import set_trace
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-connections-api")
PERSONS_API_URL = "http://udaconnect-persons-api:5000/api/persons"
LOCATIONS_PERSONS_API_URL = "http://udaconnect-locations-api:5000/api/locations/persons_and_locations?person_id={}&start_date={}&end_date={}&distance={}"

class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        # Cache all users in memory for quick lookup
        result = requests.get(PERSONS_API_URL)
        if result.status_code != 200:
            return []
        person_map: Dict[str, Person] = {person["id"]: person for person in result.json()}

        # Prepare arguments for queries
        result = requests.get(LOCATIONS_PERSONS_API_URL.format(person_id, start_date, end_date, meters))
        if result.status_code != 200:
            return []
        persons_locations: List = result.json()
        contacts: List[Connection] = []
        for person_location in persons_locations:
            location = person_location["location"]
            location['creation_time'] = datetime.strptime(location['creation_time'], '%Y-%m-%dT%H:%M:%S')
            contacts.append(Connection(
                        person=person_map[person_location['person_id']], location=person_location['location']
                    ))
        return contacts
