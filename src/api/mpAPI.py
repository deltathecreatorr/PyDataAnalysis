from mp_api.client import MPRester
from config import SERVICE_ID, USERNAME
from api.database import add_record, find_by_formula, add_dos_record, find_dos_record
import keyring
import json

def fetch_data(formula, min_band_gap=None, max_band_gap=None):
    """
    Fetches material data for a given chemical formula from the local database or the Materials Project API.

    **Arguments**
        *formula* (str)
            - The chemical formula to search for (e.g., "Fe3O4").
        *min_band_gap* (float, optional)
            - The minimum band gap in eV.
        *max_band_gap* (float, optional)
            - The maximum band gap in eV.

    **Returns**
        *dict*
            - A dictionary where keys are material IDs and values are dictionaries containing material properties 
              (e.g., formula, crystal system, band gap, etc.). Returns an empty dictionary if no materials are found.
    """
    
    try:
        formula = formula.strip()
        photocatalyst_candidates = {}

        local_records = find_by_formula(formula)
        if local_records:
            # Check if we have the new fields
            first_data = json.loads(local_records[0][1])
            if "band_gap" in first_data:
                print(f"Found {len(local_records)} records in local database.")
                for m_id, data in local_records:
                    cand = json.loads(data)
                    
                    # Filter by band gap if ranges are provided
                    bg = cand.get('band_gap')
                    if min_band_gap is not None and (bg is None or bg < min_band_gap):
                        continue
                    if max_band_gap is not None and (bg is None or bg > max_band_gap):
                        continue

                    if 'formula_pretty' not in cand:
                        cand['formula_pretty'] = formula
                    photocatalyst_candidates[m_id] = cand
                
                if photocatalyst_candidates:
                    print("Photocatalyst Candidates from local DB:", photocatalyst_candidates)
                    return photocatalyst_candidates

        api_key = keyring.get_password(SERVICE_ID, USERNAME)
        if not api_key:
            raise ValueError("API key not found. Please set your API key.")

        # Fetch data from Materials Project API
        with MPRester(api_key) as mpr:
            # Prepare band gap range for API query
            band_gap_range = None
            if min_band_gap is not None or max_band_gap is not None:
                band_gap_range = (min_band_gap if min_band_gap is not None else 0, 
                                  max_band_gap if max_band_gap is not None else 100)

            # First, get summary data to filter by formula
            materials = mpr.materials.summary.search(
                formula=formula,
                band_gap=band_gap_range,
                fields=["material_id", "formula_pretty", "band_gap", "energy_above_hull", "cbm", "vbm"]
            )
            
            for material in materials:
                m_id = str(material.material_id)
                
                # Check if DOS data is available
                try:
                    # Check local DB first
                    existing_dos = find_dos_record(m_id)
                    if not existing_dos:
                        dos = mpr.get_dos_by_material_id(m_id)
                        if not dos:
                            continue
                        # Save to local DB
                        add_dos_record(m_id, json.dumps(dos.as_dict(), default=str))
                except Exception:
                    continue

                data = {
                    "material_id": m_id,
                    "formula_pretty": material.formula_pretty,
                    "band_gap": material.band_gap,
                    "energy_above_hull": material.energy_above_hull,
                    "cbm": material.cbm,
                    "vbm": material.vbm
                }
                
                # Add to return dictionary
                photocatalyst_candidates[m_id] = data
                
                # Save to local database
                add_record(m_id, formula, json.dumps(data))

        print(f"Found {len(photocatalyst_candidates)} materials from API.")
        return photocatalyst_candidates
    except Exception as e:
        print(f"Error: {e}")
        return {}

def fetch_dos(material_id):
    try:
        # Check local DB
        local_dos = find_dos_record(material_id)
        if local_dos:
             return json.loads(local_dos)

        api_key = keyring.get_password(SERVICE_ID, USERNAME)
        if not api_key:
            raise ValueError("API key not found. Please set your API key.")

        with MPRester(api_key) as mpr:
            dos_data = mpr.get_dos_by_material_id(material_id)
            if dos_data:
                # Save it
                add_dos_record(material_id, json.dumps(dos_data.as_dict(), default=str))
                return dos_data
            else:
                print(f"No DOS data found for material ID: {material_id}")
                return None
    except Exception as e:
        print(f"Error fetching DOS data: {e}")
        return None