from datetime import datetime

from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema, LocationWithPersonIDSchema
from app.udaconnect.services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling

@api.route("/locations/persons_and_locations")
@api.param("person_id", "ID for a given Person", _in="query")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class PersonsAndLocations(Resource):
    @responds(schema=LocationWithPersonIDSchema, many=True)
    def get(self) -> LocationWithPersonIDSchema:
        person_id = request.args["person_id"]
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance = request.args["distance"]
        return LocationService.retrieve_neighboring_persons_and_locations(person_id, start_date, end_date, distance)


@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location

