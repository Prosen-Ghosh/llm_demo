from app.services.provider_manager import provider_manager
from app.services.cost_tracker import cost_tracker

def get_provider_manager():
    return provider_manager

def get_cost_tracker():
    return cost_tracker