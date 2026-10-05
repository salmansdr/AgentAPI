""" Estimation Service for project estimation details."""

from fastapi import FastAPI, HTTPException
import requests



def get_estimation(estimation_id: str):
    """
    Fetch project estimation report by estimationId using requests
    """
    url = f"https://buildproapi.onrender.com/api/ProjectEstimation/report/{estimation_id}"
    print(f"Fetching project estimation from URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling API: {str(e)}")

