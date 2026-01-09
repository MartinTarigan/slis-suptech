from typing import List, Dict, Any, Tuple

from .names import calculate_advanced_name_score
from .dob import calculate_dob_score_structured, parse_dob
from .geo import generate_geographic_insights
from .utils import normalize_and_compare



BASE_WEIGHTS = {
    "name": 0.50,         
    "dob": 0.35,          
    "citizenship": 0.15,  
}


def _extract_customer_fields(customer: Dict[str, Any]) -> Dict[str, Any]:
    name = (
        customer.get("Nama")
        or customer.get("Full_Name")
        or customer.get("full_name")
        or customer.get("name")
    )

    dob = (
        customer.get("Tanggal Lahir")
        or customer.get("Tanggal_Lahir")
        or customer.get("Date_of_Birth")
        or customer.get("dob")
    )

    citizenship = (
        customer.get("Kewarganegaraan")
        or customer.get("Citizenship")
        or customer.get("citizenship")
    )

    country_of_residence = (
        customer.get("Country_of_Residence")
        or customer.get("country_of_residence")
        or customer.get("Residence")
    )

    place_of_birth = (
        customer.get("Place_of_Birth")
        or customer.get("Tempat_Lahir")
        or customer.get("place_of_birth")
    )

    return {
        "name": name or "",
        "dob": dob or "",
        "citizenship": citizenship or "",
        "country_of_residence": country_of_residence or "",
        "place_of_birth": place_of_birth or "",
    }


def _extract_sanction_fields(sanction: Dict[str, Any]) -> Dict[str, Any]:
    full_name = (
        sanction.get("Full_Name")
        or sanction.get("full_name")
        or sanction.get("Name")
        or sanction.get("name")
    )

    dob_struct = sanction.get("dob_struct")

    date_of_birth_raw = (
        sanction.get("Date_of_Birth") or sanction.get("dob") or sanction.get("Tanggal_Lahir") or sanction.get("dob_raw")
    )

    citizenship = (
        sanction.get("Citizenship")
        or sanction.get("citizenship")
        or sanction.get("Kewarganegaraan")
    )

    source = sanction.get("Source_List") or sanction.get("source") or "N/A"

    return {
        "full_name": full_name or "",
        "dob_struct": dob_struct,
        "date_of_birth_raw": date_of_birth_raw or "",
        "citizenship": citizenship or "",
        "source_list": source,
    }


def _compute_dynamic_weights(
    has_dob: bool,
    has_citizenship: bool,
) -> Tuple[str, Dict[str, float]]:
    """
    Menentukan skema bobot & bobot ter-normalisasi berdasarkan
    field yang tersedia untuk pasangan customer–sanction ini.

    Return:
        scheme_name: string deskriptif (mis. "name_dob", "name_only")
        weights: dict { "name": w_name, "dob": w_dob, "citizenship": w_cit }
                 (hanya key yg dipakai yang muncul; total = 1.0)
    """
    
    components: Dict[str, float] = {
        "name": BASE_WEIGHTS["name"],
    }

    if has_dob:
        components["dob"] = BASE_WEIGHTS["dob"]

    if has_citizenship:
        components["citizenship"] = BASE_WEIGHTS["citizenship"]

    total = sum(components.values())
    if total <= 0:
        # fallback defensif
        return "invalid", {"name": 1.0}

    normalized = {k: v / total for k, v in components.items()}

    if has_dob and has_citizenship:
        scheme_name = "name_dob_citizenship"
    elif has_dob and not has_citizenship:
        scheme_name = "name_dob"
    elif not has_dob and has_citizenship:
        scheme_name = "name_citizenship"
    else:
        scheme_name = "name_only"

    return scheme_name, normalized


def run_screening_engine(
    customers: List[Dict[str, Any]],
    sanctions: List[Dict[str, Any]],
    name_threshold: float = 70.0,
) -> List[Dict[str, Any]]:

    results: List[Dict[str, Any]] = []

    processed_customers = []
    for cust in customers:
        fields = _extract_customer_fields(cust)
        if not fields["name"]: continue
        
        # Parse DOB Customer ke Structured Dict
        fields["dob_struct"] = parse_dob(fields["dob"])
        processed_customers.append({"original": cust, "fields": fields})

    processed_sanctions = []
    for sanc in sanctions:
        fields = _extract_sanction_fields(sanc)
        if not fields["full_name"]: continue

        # Jika caller belum menyediakan dob_struct, parse sekarang
        if not fields["dob_struct"]:
            fields["dob_struct"] = parse_dob(fields["date_of_birth_raw"])
            
        processed_sanctions.append({"original": sanc, "fields": fields})

    for cust_obj in processed_customers:
        cust_fields = cust_obj["fields"]
        cust_origin = cust_obj["original"]
        customer_name = cust_fields["name"]

        for sanc_obj in processed_sanctions:
            sanc_fields = sanc_obj["fields"]
            sanc_origin = sanc_obj["original"]

            name_score = calculate_advanced_name_score(customer_name, sanc_fields["full_name"])
            if name_score < name_threshold: continue

            # --- DOB Matching (Structured) ---
            # Syarat: Customer punya Year DAN Sanction punya Year
            cust_dob = cust_fields["dob_struct"]
            sanc_dob = sanc_fields["dob_struct"]
            
            has_dob = bool(cust_dob.get("year") and sanc_dob.get("year"))
            
            dob_score = 0.0
            dob_match_type = "Not Available"

            if has_dob:
                score, desc = calculate_dob_score_structured(
                    cust_dob=cust_dob,
                    sanction_dob=sanc_dob,
                    raw_sanction_str=sanc_fields["date_of_birth_raw"],
                    source_code=sanc_fields["source_list"]
                )
                dob_score = float(score)
                dob_match_type = desc

            # --- Citizenship Matching ---
            has_cit = bool(cust_fields["citizenship"] and sanc_fields["citizenship"])
            citizenship_score = 0.0
            if has_cit:
                citizenship_score = normalize_and_compare(
                    cust_fields["citizenship"],
                    sanc_fields["citizenship"],
                )

            # --- Final Score ---
            scheme_name, weights = _compute_dynamic_weights(has_dob, has_cit)

            final_score = (
                weights.get("name", 0.0) * name_score
                + weights.get("dob", 0.0) * dob_score
                + weights.get("citizenship", 0.0) * citizenship_score
            )

            # Geo Insights
            geo_insights = generate_geographic_insights(
                {
                    "Citizenship": cust_fields["citizenship"],
                    "Country_of_Residence": cust_fields["country_of_residence"],
                    "Place_of_Birth": cust_fields["place_of_birth"],
                },
                {"Citizenship": sanc_fields["citizenship"]}
            )

            exact_matches_found = []
            if has_dob and dob_score > 0:
                exact_matches_found.append(f"Date_of_Birth ({dob_match_type})")
            if has_cit and citizenship_score == 100:
                exact_matches_found.append("Citizenship")

            results.append({
                "Customer_Id": cust_origin.get("id") or cust_origin.get("customer_id"),
                "Sanction_Id": sanc_origin.get("id") or sanc_origin.get("sanction_id"),
                "Customer_Name": customer_name,
                "Matched_Sanction_Name": sanc_fields["full_name"],
                "Source_List": sanc_fields["source_list"],
                "Final_Score": final_score,
                "Name_Score": name_score,
                "DOB_Score": dob_score,
                "DOB_Match_Type": dob_match_type,
                "Citizenship_Score": citizenship_score,
                "Customer_DOB": cust_fields["dob"],
                "Sanction_DOB": sanc_fields["date_of_birth_raw"],
                "Customer_Citizenship": cust_fields["citizenship"],
                "Sanction_Citizenship": sanc_fields["citizenship"],
                "Exact_Matches": ", ".join(exact_matches_found) if exact_matches_found else "None",
                "Geographic_Insights": geo_insights,
                "Weighting_Scheme": scheme_name,
                "Weights_Used": weights,
                "Has_DOB": has_dob,
                "Has_Citizenship": has_cit,
            })

    return results