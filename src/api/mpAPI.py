from mp_api.client import MPRester
from config import SERVICE_ID, USERNAME
from api.database import add_record, find_record, remove_record, find_by_formula
from config import OFFLINE_MODE
import keyring
import json

def fetch_data(formula):
    try:
        formula = formula.strip()
        magnetic_candidates = {}

        # Check local database first
        local_records = find_by_formula(formula)
        if local_records:
            print(f"Found {len(local_records)} records in local database.")
            for m_id, data in local_records:
                magnetic_candidates[m_id] = json.loads(data)
            print("Magnetic Candidates from local DB:", magnetic_candidates)
            return magnetic_candidates

        if OFFLINE_MODE:
            print("Offline mode is enabled. Skipping API calls.")
            return magnetic_candidates

        api_key = keyring.get_password(SERVICE_ID, USERNAME)
        if not api_key:
            raise ValueError("API key not found. Please set your API key.")

        with MPRester(api_key) as mpr:
            materials = mpr.materials.summary.search(formula=formula)
            materials_ids = [(str(material.material_id), material.formula_pretty) for material in materials]
            print(materials_ids)

            ids_to_fetch = []
            for m_id, _ in materials_ids:
                record = find_record(m_id)
                if record:
                    magnetic_candidates[m_id] = json.loads(record)
                else:
                    ids_to_fetch.append(m_id)

            if ids_to_fetch:
                magnets = mpr.materials.magnetism.search(
                    material_ids=ids_to_fetch,
                    fields=["material_id","formula_pretty", "total_magnetization", "ordering"]
                )
                for material in magnets:
                    if material.total_magnetization and abs(material.total_magnetization) > 0.1:
                        data = {
                            "strength": round(material.total_magnetization, 3),
                            "type": material.ordering,
                        }
                        m_id_str = str(material.material_id)
                        magnetic_candidates[m_id_str] = data
                        add_record(m_id_str, material.formula_pretty, json.dumps(data))
            
        print("Magnetic Candidates:", magnetic_candidates)
    except Exception as e:
        print(f"Error: {e}")