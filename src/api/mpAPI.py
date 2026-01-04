from mp_api.client import MPRester
from config import SERVICE_ID, USERNAME
from api.database import add_record, find_record, remove_record, find_by_formula
from config import OFFLINE_MODE
import keyring
import json

def fetch_data(formula):
    """
    Fetches material data for a given chemical formula from the local database or the Materials Project API.

    **Arguments**
        *formula* (str)
            - The chemical formula to search for (e.g., "Fe3O4").

    **Returns**
        *dict*
            - A dictionary where keys are material IDs and values are dictionaries containing material properties 
              (e.g., formula, crystal system, band gap, etc.). Returns an empty dictionary if no materials are found.
    """
    
    try:
        formula = formula.strip()
        magnetic_candidates = {}

        local_records = find_by_formula(formula)
        if local_records:
            # Check if we have the new fields
            first_data = json.loads(local_records[0][1])
            if "crystal_system" in first_data:
                print(f"Found {len(local_records)} records in local database.")
                for m_id, data in local_records:
                    cand = json.loads(data)
                    if 'formula_pretty' not in cand:
                        cand['formula_pretty'] = formula
                    magnetic_candidates[m_id] = cand
                print("Magnetic Candidates from local DB:", magnetic_candidates)
                return magnetic_candidates

        #Check if the user wants to be in offline mode
        if OFFLINE_MODE:
            print("Offline mode is enabled. Skipping API calls.")
            return magnetic_candidates

        api_key = keyring.get_password(SERVICE_ID, USERNAME)
        if not api_key:
            raise ValueError("API key not found. Please set your API key.")

        # Fetch data from Materials Project API
        with MPRester(api_key) as mpr:
            # First, get summary data to filter by formula
            materials = mpr.materials.summary.search(
                formula=formula,
                fields=["material_id", "formula_pretty", "symmetry", "nsites", "energy_above_hull", "band_gap"]
            )
            
            # Use JSON to store summary data for quick access
            summary_data = {}
            for material in materials:  
                m_id = str(material.material_id)
                summary_data[m_id] = {
                    "spacegroup_symbol": material.symmetry.symbol if material.symmetry else None,
                    "num_sites": material.nsites,
                    "energy_above_hull": material.energy_above_hull,
                    "band_gap": material.band_gap
                }

            materials_ids = [(str(material.material_id), material.formula_pretty) for material in materials]
            print(materials_ids)

            # Now, check local DB for magnetism data
            ids_to_fetch = []
            for m_id, formula_pretty in materials_ids:
                record = find_record(m_id)
                if record:
                    data = json.loads(record)
                    if 'formula_pretty' not in data:
                        data['formula_pretty'] = formula_pretty
                    
                    if m_id in summary_data:
                        data.update(summary_data[m_id])
                        add_record(m_id, formula_pretty, json.dumps(data))

                    magnetic_candidates[m_id] = data
                else:
                    ids_to_fetch.append(m_id)

            # Fetch magnetism data for missing records from Materials Project API
            if ids_to_fetch:
                magnets = mpr.materials.magnetism.search(
                    material_ids=ids_to_fetch,
                    fields=["material_id","formula_pretty", "total_magnetization_normalized_formula_units", "is_magnetic", "ordering"]
                )
                for material in magnets:
                    if not material.is_magnetic:
                        continue
                    if material.total_magnetization_normalized_formula_units is None:
                        continue
                    if material.total_magnetization_normalized_formula_units <= 0:
                        continue
                    if material.ordering == "NM" or material.ordering == "AFM":
                        continue
                    data = {
                        "normalized_magnetisation_units": round(material.total_magnetization_normalized_formula_units, 6),
                        "is_magnetic": bool(material.is_magnetic),
                        "type": material.ordering,
                        "formula_pretty": material.formula_pretty,
                    }
                    m_id_str = str(material.material_id)
                    
                    if m_id_str in summary_data:
                        data.update(summary_data[m_id_str])

                    magnetic_candidates[m_id_str] = data
                    add_record(m_id_str, material.formula_pretty, json.dumps(data))
            
        print("Magnetic Candidates:", magnetic_candidates)
        return magnetic_candidates
    except Exception as e:
        print(f"Error: {e}")
        return {}