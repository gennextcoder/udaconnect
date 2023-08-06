from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from datetime import datetime
from kafka import KafkaConsumer

from config import DATABASE_URI
from models import Location
from schema import LocationSchema
from geoalchemy2.functions import ST_Point
from contextlib import contextmanager

import json
import logging

TOPIC_NAME = 'locations'
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers="kafka:9092")

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def consume():
    for message in consumer:
        try:
            location = json.loads(message.value.decode("utf-8"))
            print(location)
            validation_results: Dict = LocationSchema().validate(location)
            if validation_results:
                print(f"Unexpected data format in payload: {validation_results}")
                return
            new_location = Location()
            new_location.id = location["id"]
            new_location.person_id = location["person_id"]
            new_location.creation_time = location["creation_time"]
            new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
            with session_scope() as db:
                db.add(new_location)
        except Exception as e:
            logging.exception("Exception occured!")


if __name__ == '__main__':
    consume()