from mp_api.client import MPRester
from config import SERVICE_ID, USERNAME
from api.database import add_record, find_record, remove_record
import keyring
import json

def fetch_data(formula):
    try:
        api_key = keyring.get_password(SERVICE_ID, USERNAME)
        if not api_key:
            raise ValueError("API key not found. Please set your API key.")
        
        magnetic_candidates = {}

        with MPRester(api_key) as mpr:
            formula = formula.strip()
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