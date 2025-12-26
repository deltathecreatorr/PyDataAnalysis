from mp_api.client import MPRester
from config import SERVICE_ID, USERNAME
import keyring

def fetch_data():
    try:
        api_key = keyring.get_password(SERVICE_ID, USERNAME)
        if not api_key:
            raise ValueError("API key not found. Please set your API key.")
        
        magnetic_candidates = {}

        with MPRester(api_key) as mpr:
            formula = "Ac2MgSn"
            materials = mpr.materials.summary.search(formula=formula)
            materials_ids = [(material.material_id, material.formula_pretty) for material in materials]
            print(materials_ids)

            magnets = mpr.materials.magnetism.search(
                material_ids=[material_id for material_id, _ in materials_ids],
                fields=["material_id","elements", "total_magnetization", "ordering"]
            )
            for material in magnets:
                if material.total_magnetization and abs(material.total_magnetization) > 0.1:
                
                    magnetic_candidates[material.material_id] = {
                        "strength": round(material.total_magnetization, 3),
                        "type": material.ordering  # e.g., 'FM', 'FiM'
                    }
            
        print("Magnetic Candidates:", magnetic_candidates)
    except Exception as e:
        print(f"Error: {e}")