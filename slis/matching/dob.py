import re
from typing import Dict, Any, List


def parse_dob(dob_string: str) -> Dict[str, Any]:
    """
    Mengekstrak tahun, bulan, dan hari dari string DOB.
    Support format:
    - YYYY
    - YYYY-MM
    - YYYY-MM-DD
    - Format Indonesia (20 Juli 1985, dsb)
    - Delimiter: -, /, ., spasi
    """
    if not isinstance(dob_string, str) or not dob_string.strip():
        return {'year': None, 'month': None, 'day': None}

    dob_string = dob_string.lower()
    dob_string = (
        dob_string.replace('januari', '01')
        .replace('februari', '02')
        .replace('maret', '03')
        .replace('april', '04')
        .replace('mei', '05')
        .replace('juni', '06')
        .replace('juli', '07')
        .replace('agustus', '08')
        .replace('september', '09')
        .replace('oktober', '10')
        .replace('november', '11')
        .replace('desember', '12')
    )

    parts = re.split(r'[-/.\s]', dob_string.strip())
    year = month = day = None

    for part in parts:
        if not part.isdigit():
            continue
        value = int(part)
        if len(part) == 4 and year is None:
            year = value
        elif 1 <= value <= 12 and month is None:
            month = value
        elif 1 <= value <= 31 and day is None:
            day = value

    return {'year': year, 'month': month, 'day': day}


def get_years_from_sanction_dob(dob_string: str) -> List[Dict[str, Any]]:
    """
    Mengambil daftar tahun atau rentang tahun dari string DOB sanksi (Australia).
    Contoh:
    - "1980-1985" -> [{'min': 1980, 'max': 1985, 'type': 'range'}]
    - "1980, 1985" -> [{'year': 1980, 'type': 'single'}, {'year': 1985, 'type': 'single'}]
    """
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
                year_data.append({
                    'min': min(year1, year2),
                    'max': max(year1, year2),
                    'type': 'range'
                })
                i += 2
                continue

        year_data.append({'year': year1, 'type': 'single'})
        i += 1

    unique_year_data = []
    seen = set()
    for entry in year_data:
        key = tuple(sorted(entry.items()))
        if key not in seen:
            unique_year_data.append(entry)
            seen.add(key)

    return unique_year_data


def calculate_dob_score_flexible(
    customer_dob_str: str,
    sanction_dob_str: str,
    source_list: str
):
    """
    Menghitung skor DOB:
    - Untuk Australia: year range -> Full Match = 100
    - Untuk lainnya:
        - Full match (Y, M, D)  = 100
        - Year & Month match    = 75
        - Year-only match       = 50
        - No match              = 0
    Return: (score, description)
    """
    customer_dob_parsed = parse_dob(customer_dob_str)
    cust_year = customer_dob_parsed['year']

    if cust_year is None:
        return 0, "No Customer DOB"

    # Logika Australia (fleksibel)
    if "Australia" in str(source_list):
        sanction_years = get_years_from_sanction_dob(sanction_dob_str)
        if not sanction_years:
            return 0, "No Sanction DOB / Unparsable (Australia)"

        for entry in sanction_years:
            if entry['type'] == 'single' and entry['year'] == cust_year:
                return 100, "Full Match (Australia - Single Year)"
            elif entry['type'] == 'range' and entry['min'] <= cust_year <= entry['max']:
                return 100, f"Full Match (Australia - Range: {entry['min']}-{entry['max']})"

        return 0, "No Match (Australia)"

    p2 = parse_dob(sanction_dob_str)
    sanction_year = p2['year']

    if sanction_year is None or cust_year != sanction_year:
        return 0, "No Match"

    has_month1, has_month2 = customer_dob_parsed['month'] is not None, p2['month'] is not None
    if not has_month1 or not has_month2 or customer_dob_parsed['month'] != p2['month']:
        return 50, "Year Match"

    has_day1, has_day2 = customer_dob_parsed['day'] is not None, p2['day'] is not None
    if not has_day1 or not has_day2 or customer_dob_parsed['day'] != p2['day']:
        return 75, "Year & Month Match"

    return 100, "Full Match"
