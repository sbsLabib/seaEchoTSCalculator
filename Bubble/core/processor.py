# core/processor.py
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from functools import partial  # <-- Critical import
from utils.SeaEcho_water_bubble import seawater, air_bubble
from utils.physical_properties import sound_speed

# Model imports (from your file structure)
from models.medwin_clay_model import calculate_medwin_clay_ts
from models.breathing_model import calculate_breathing_ts
from models.thuraisingham_model import calculate_thuraisingham_ts
from models.modal_solution import calculate_modal_ts
from models.weston_medwin_model import calculate_wm_ts
from models.anderson_weston_model import calculate_aw_ts
from models.ainslie_leighton_model import calculate_ainslie_leighton_ts

MODEL_FUNCTIONS = {
    "Medwin_Clay": calculate_medwin_clay_ts,
    "Breathing": calculate_breathing_ts,
    "Thuraisingham": calculate_thuraisingham_ts,
    "Modal": calculate_modal_ts,
    "Weston_Medwin": calculate_wm_ts,
    "Anderson_Weston": calculate_aw_ts,
    "Ainslie_Leighton": calculate_ainslie_leighton_ts
}

def _process_wrapper(f, water_params, bubble_params, c, models):
    """Reconstruct objects using positional arguments"""
    # Recreate seawater from tuple (T, z, S)
    water = seawater(*water_params)
    
    # Recreate bubble using (water, T, z, S, d)
    bubble = air_bubble(water, *bubble_params)
    
    return _process_single_frequency(f, water, bubble, c, models)

def _process_single_frequency(f, water, bubble, c, models):
    """Core TS calculation logic"""
    k = 2 * np.pi * f * 1000 / c
    a = bubble.d / 2
    ka = k * a
    
    ts_values = {"ka": ka}
    for model in models:
        ts_values[model] = MODEL_FUNCTIONS[model](f, c, water, bubble)
    
    return ts_values

def run_calculations(params):
    """Parallel execution coordinator"""
    # Initialize objects (unchanged)
    water = seawater(params['T'], params['z'], params['S'])
    bubble = air_bubble(water, params['T'], params['z'], params['S'], params['d'])
    c = sound_speed(params['T'], params['S'], params['z'])
    
    # Prepare parameters as tuples for positional arguments
    water_params = (params['T'], params['z'], params['S'])
    bubble_params = (params['T'], params['z'], params['S'], params['d'])
    
    # Create partial function
    processor = partial(
        _process_wrapper,
        water_params=water_params,
        bubble_params=bubble_params,
        c=c,
        models=params['models']
    )
    
    # Execute in parallel
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(processor, params['frequencies']))
    
    # Organize results into dictionary format
    processed = {
        'ka': np.array([res['ka'] for res in results]),
        'ts': {model: np.array([res[model] for res in results]) 
               for model in params['models']}
    }
    
    return {
        'params': params,
        'results': processed,  # Now a DICT with 'ka' and 'ts' keys
        'environment': {'water': water, 'bubble': bubble, 'c': c}
    }