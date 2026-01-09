import re
from typing import Dict, Any, List, Tuple
from datetime import date, datetime

# --- 1. PARSER INPUT (String -> Dict) ---
def parse_dob(dob_input: Any) -> Dict[str, Any]:
    """
    Parser robust untuk mengubah input string (dari UI/Excel) menjadi structured dict.
    Output: {'year': 1996, 'month': 7, 'day': 30}
    """
    # Handle jika input sudah datetime object
    if isinstance(dob_input, (date, datetime)):
        return {'year': dob_input.year, 'month': dob_input.month, 'day': dob_input.day}
        
    if not dob_input or not isinstance(dob_input, str) or not dob_input.strip():
        return {'year': None, 'month': None, 'day': None}

    dob_string = dob_input.lower().strip()
    
    # Mapping Bulan Indonesia & Inggris
    month_map = {
        'januari': '01', 'februari': '02', 'maret': '03', 'april': '04',
        'mei': '05', 'juni': '06', 'juli': '07', 'agustus': '08',
        'september': '09', 'oktober': '10', 'november': '11', 'desember': '12',
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
        'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }
    
    for name, digit in month_map.items():
        if name in dob_string:
            dob_string = dob_string.replace(name, digit)
    
    # Split angka
    parts = re.split(r'[-/.\s]+', dob_string)
    parts = [int(p) for p in parts if p.isdigit()]
    
    year, month, day = None, None, None

    # Logic Heuristik Posisi
    if len(parts) == 3:
        p1, p2, p3 = parts[0], parts[1], parts[2]
        if p1 > 1000: 
            year, month, day = p1, p2, p3 # YYYY-MM-DD
        elif p3 > 1000: 
            year = p3 # DD-MM-YYYY
            if p2 > 12: month, day = p1, p2 # US Style
            else: day, month = p1, p2       # Indo Style
    elif len(parts) == 1 and parts[0] > 1000:
        year = parts[0]

    # Validasi Range
    if month and (month < 1 or month > 12): month = None
    if day and (day < 1 or day > 31): day = None
            
    return {'year': year, 'month': month, 'day': day}

# --- 2. AUSTRALIA HELPER (String Range Logic) ---
def get_years_from_sanction_dob(dob_string: str) -> List[Dict[str, Any]]:
    if not isinstance(dob_string, str) or not dob_string.strip():
        return []
    dob_string = dob_string.strip().replace(',', '-')
    potential_years = re.findall(r'\d{4}', dob_string)
    year_data = []
    i = 0
    while i < len(potential_years):
        year1 = int(potential_years[i])
        if i + 1 < len(potential_years):
            year2 = int(potential_years[i + 1])
            if re.search(f"{year1}-{year2}", dob_string) or re.search(f"{year2}-{year1}", dob_string):
                year_data.append({'min': min(year1, year2), 'max': max(year1, year2), 'type': 'range'})
                i += 2
                continue
        year_data.append({'year': year1, 'type': 'single'})
        i += 1
    return year_data

# --- 3. SCORING ENGINE (Structured Integer Comparison) ---
def calculate_dob_score_structured(
    cust_dob: Dict[str, int],      
    sanction_dob: Dict[str, int],  
    raw_sanction_str: str,         
    source_code: str
) -> Tuple[float, str]:
    """
    Membandingkan DOB User (Dict) vs DOB Sanksi (Dict) menggunakan integer.
    """
    c_y = cust_dob.get('year')
    c_m = cust_dob.get('month')
    c_d = cust_dob.get('day')
    
    if not c_y:
        return 0.0, "No Customer DOB Year"

    # A. LOGIKA AUSTRALIA (Range Support)
    if source_code and "Australia" in str(source_code):
        sanction_years = get_years_from_sanction_dob(raw_sanction_str or "")
        if sanction_years:
            for entry in sanction_years:
                if entry['type'] == 'single' and entry['year'] == c_y:
                    return 100.0, "Full Match (Australia Year)"
                elif entry['type'] == 'range' and entry['min'] <= c_y <= entry['max']:
                    return 100.0, f"Full Match (Australia Range: {entry['min']}-{entry['max']})"
        # Fallback ke logic standar jika range gagal

    # B. LOGIKA STANDAR (Integer Match)
    s_y = sanction_dob.get('year')
    s_m = sanction_dob.get('month')
    s_d = sanction_dob.get('day')

    # 1. Cek Tahun
    if not s_y: return 0.0, "No Sanction Year Data"
    if c_y != s_y: return 0.0, f"Year Mismatch ({c_y} vs {s_y})"

    # 2. Cek Bulan (Partial Logic)
    if not c_m or not s_m: return 50.0, "Year Match (Month Missing)"
    if c_m != s_m: return 50.0, "Year Match (Month Mismatch)"
    
    # 3. Cek Hari (Full Logic)
    if not c_d or not s_d: return 75.0, "Year & Month Match (Day Missing)"
    if c_d != s_d: return 75.0, "Year & Month Match (Day Mismatch)"

    return 100.0, "Full Match"