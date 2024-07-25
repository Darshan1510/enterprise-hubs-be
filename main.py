from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from typing import Optional, List
from geopy.distance import geodesic
import logging
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Company Locations API",
    description="API for managing company and location data",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Companies",
            "description": "Operations with companies."
        },
        {
            "name": "Locations",
            "description": "Operations with locations."
        }
    ]
)

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load CSV files
try:
    companies_df = pd.read_csv('companies.csv')
    locations_df = pd.read_csv('locations.csv')
    logger.info("CSV files loaded successfully.")
except Exception as e:
    logger.error(f"Error loading CSV files: {e}")
    raise HTTPException(status_code=500, detail="Internal server error while loading data.")

class Company(BaseModel):
    """
    Pydantic model representing a company.
    """
    company_id: int
    name: str
    address: str
    latitude: float
    longitude: float

class Location(BaseModel):
    """
    Pydantic model representing a location.
    """
    location_id: int
    company_id: int
    name: str
    address: str
    latitude: float
    longitude: float

@app.get('/api/companies', response_model=List[Company], tags=["Companies"])
async def get_companies(
    name: Optional[str] = Query(None, description="Filter companies by name (case-insensitive)"),
    latitude: Optional[float] = Query(None, description="Latitude for radius search"),
    longitude: Optional[float] = Query(None, description="Longitude for radius search"),
    radius: Optional[float] = Query(10.0, description="Radius in kilometers for location-based search")
):
    """
    Retrieve a list of companies.

    - **name**: Optional filter to search companies by name.
    - **latitude**: Optional latitude for location-based search.
    - **longitude**: Optional longitude for location-based search.
    - **radius**: Optional radius in kilometers for location-based search (default is 10.0 km).
    """
    if name:
        filtered_companies = companies_df[companies_df['name'].str.contains(name, case=False, na=False)]
    elif latitude is not None and longitude is not None:
        def is_within_radius(row, center, radius):
            company_location = (row['latitude'], row['longitude'])
            return geodesic(company_location, center).km <= radius

        center = (latitude, longitude)
        filtered_companies = companies_df[companies_df.apply(lambda row: is_within_radius(row, center, radius), axis=1)]
    else:
        filtered_companies = companies_df

    companies = [Company(**company) for company in filtered_companies.to_dict(orient='records')]
    return companies

@app.get('/api/companies/{company_id}', response_model=Company, tags=["Companies"])
async def get_company(company_id: int):
    """
    Retrieve a company by its ID.

    - **company_id**: The ID of the company to retrieve.
    """
    company = companies_df[companies_df['company_id'] == company_id].to_dict(orient='records')
    if company:
        return Company(**company[0])
    else:
        logger.warning(f"Company with ID {company_id} not found.")
        raise HTTPException(status_code=404, detail='Company not found')

@app.get('/api/companies/{company_id}/locations', response_model=List[Location], tags=["Locations"])
async def get_locations(company_id: int):
    """
    Retrieve all locations for a specific company ID.

    - **company_id**: The ID of the company whose locations to retrieve.
    """
    locations = locations_df[locations_df['company_id'] == company_id].to_dict(orient='records')
    if locations:
        return [Location(**location) for location in locations]
    else:
        logger.warning(f"No locations found for company ID {company_id}.")
        raise HTTPException(status_code=404, detail='Locations not found')

@app.get('/api/healthcheck', tags=["Health Check"])
async def healthcheck():
    """
    Perform a health check on the API.
    """
    return JSONResponse(content={'status': 'ok'})

@app.get('/', tags=["Hello world"])
async def healthcheck():
    """
    Test Hello world API.
    """
    return JSONResponse(content={'message': 'Hello World'})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
