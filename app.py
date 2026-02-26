import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from pdf_report import generate_pdf

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BVI Flag Suitability Tool",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

:root {
    --navy: #0d2137;
    --navy-mid: #163354;
    --gold: #c9a84c;
    --gold-light: #e8c97a;
    --red: #c0392b;
    --white: #f8f6f1;
    --grey: #8a9bb0;
    --light-bg: #f0ede6;
}

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: var(--white);
    color: var(--navy);
}

.main { background-color: var(--white); }
.block-container { padding: 2rem 3rem; max-width: 1100px; }

h1, h2, h3 { font-family: 'Playfair Display', serif; }

.hero {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 60%, #1e4a7a 100%);
    border-radius: 16px;
    padding: 3rem 3.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(201,168,76,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    color: var(--white);
    font-size: 2.4rem;
    margin: 0 0 0.5rem 0;
    line-height: 1.2;
}
.hero .subtitle {
    color: var(--gold-light);
    font-size: 1.05rem;
    font-weight: 300;
    margin: 0;
}
.hero .ensign {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
}

.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: var(--navy);
    border-left: 4px solid var(--gold);
    padding-left: 1rem;
    margin: 2rem 0 1.2rem 0;
}

.group-card {
    background: white;
    border: 1px solid #ddd8ce;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(13,33,55,0.06);
}
.group-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: var(--navy-mid);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.profile-card {
    background: white;
    border: 1px solid #ddd8ce;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(13,33,55,0.06);
}

.score-hero {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 100%);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    color: white;
}
.score-number {
    font-family: 'Playfair Display', serif;
    font-size: 5rem;
    color: var(--gold-light);
    line-height: 1;
    margin: 0.5rem 0;
}
.score-label {
    font-size: 1rem;
    color: rgba(255,255,255,0.7);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.score-verdict {
    font-size: 1.4rem;
    font-family: 'Playfair Display', serif;
    color: white;
    margin-top: 0.5rem;
}

.factor-row {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #eee;
}
.factor-row:last-child { border-bottom: none; }
.factor-name {
    font-weight: 600;
    color: var(--navy);
    min-width: 220px;
    font-size: 0.95rem;
}
.factor-score-bar {
    flex: 1;
}
.factor-remark {
    font-size: 0.88rem;
    color: #555;
    line-height: 1.5;
    margin-top: 0.4rem;
}

.pill {
    display: inline-block;
    background: var(--light-bg);
    border: 1px solid #ddd8ce;
    border-radius: 20px;
    padding: 0.25rem 0.8rem;
    font-size: 0.8rem;
    color: var(--navy-mid);
    margin: 0.2rem;
}
.pill-gold {
    background: rgba(201,168,76,0.15);
    border-color: var(--gold);
    color: #7a5c10;
}

.cta-box {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 100%);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    color: white;
    margin-top: 2rem;
}
.cta-box h3 {
    color: var(--gold-light);
    margin-bottom: 0.5rem;
}

.stSlider > div > div { accent-color: var(--gold) !important; }
.stSelectbox > div > div { border-color: #ddd8ce !important; }

div[data-testid="stForm"] { border: none; }

.step-indicator {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 2rem;
    align-items: center;
}
.step {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 600;
    border: 2px solid #ddd;
    color: #aaa;
}
.step.active {
    background: var(--navy);
    border-color: var(--navy);
    color: white;
}
.step.done {
    background: var(--gold);
    border-color: var(--gold);
    color: white;
}
.step-line {
    flex: 1; height: 2px;
    background: #ddd;
}
.step-line.done { background: var(--gold); }

.warning-box {
    background: #fff8e6;
    border: 1px solid var(--gold);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-size: 0.9rem;
    color: #7a5c10;
    margin: 0.5rem 0;
}
.info-box {
    background: #e8f0f8;
    border: 1px solid #b0c8e0;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-size: 0.9rem;
    color: var(--navy-mid);
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────

ELIGIBLE_JURISDICTIONS = [
    "Andorra", "Argentina", "Aruba", "Bahrain", "Brazil",
    "Canary Islands (Spain)", "Chile", "China", "Switzerland",
    "United Arab Emirates", "United States of America", "Mexico", "Monaco",
    "Panama", "Republic of Korea (South Korea)", "Slovenia", "Suriname",
    "Uruguay", "Israel", "Japan", "Liberia", "Madeira (Portugal)",
    "Marshall Islands", "European Union",
    # Commonwealth
    "Antigua and Barbuda", "Australia", "Bahamas", "Bangladesh", "Barbados",
    "Belize", "Botswana", "Brunei Darussalam", "Canada", "Cameroon",
    "Cyprus", "Dominica", "Fiji", "Gambia", "Gabon", "Ghana", "Guyana",
    "Grenada", "India", "Jamaica", "Kenya", "Kingdom of Eswatini",
    "Kiribati", "Lesotho", "Malawi", "Malaysia", "Maldives", "Malta",
    "Mauritius", "Mozambique", "Namibia", "Nauru", "New Zealand",
    "Nigeria", "Pakistan", "Papua New Guinea", "Rwanda", "Samoa",
    "Seychelles", "Sierra Leone", "Singapore", "Solomon Islands",
    "South Africa", "Sri Lanka", "St. Kitts & Nevis", "St. Lucia",
    "St. Vincent & the Grenadines", "Togo", "Tonga", "Trinidad & Tobago",
    "Tuvalu", "Uganda", "United Republic of Tanzania", "United Kingdom",
    "Vanuatu", "Zambia",
    # UK
    "England", "Scotland", "Wales", "Northern Ireland",
    # Crown Dependencies
    "Bailiwick of Jersey", "Bailiwick of Guernsey", "Isle of Man",
    # British Overseas Territories
    "Anguilla", "Bermuda", "British Virgin Islands", "Cayman Islands",
    "Falkland Islands", "Gibraltar", "Montserrat", "Turks and Caicos",
    # EU Members
    "Austria", "Belgium", "Bulgaria", "Croatia", "Czech Republic",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
    "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Spain",
    "Sweden",
    # EEA
    "Iceland", "Liechtenstein", "Norway",
    # UAE
    "Abu Dhabi", "Dubai", "Sharjah", "Ajman", "Ras Al Khaimah",
    "Umm Al Quwain", "Fujairah",
    # US Territories
    "Guam", "Puerto Rico", "U.S. Virgin Islands", "American Samoa",
    "Northern Mariana Islands",
    # France Territories
    "French Polynesia", "Guadeloupe", "Martinique", "Mayotte",
    "New Caledonia", "Réunion", "Saint Barthélemy (St. Barts)",
    "Saint Martin",
    # Netherlands Territories
    "Aruba", "Bonaire", "Curacao", "Saba", "Sint Maarten", "Sint Eustatius",
    # Denmark Territories
    "Faroe Islands", "Greenland",
    # Spain Territories
    "Balearic Islands", "Ceuta and Melilla",
    # OECS
    "Commonwealth of Dominica",
]
ELIGIBLE_JURISDICTIONS = sorted(list(set(ELIGIBLE_JURISDICTIONS)))

# VAT matrix: (ubo_residency, vessel_use, cruising_area) -> score
VAT_MATRIX = {
    ("EU", "Pleasure", "EU"): 2,
    ("EU", "Pleasure", "USA"): 4,
    ("EU", "Pleasure", "Caribbean"): 5,
    ("EU", "Pleasure", "Middle East"): 4,
    ("EU", "Pleasure", "Asia"): 5,
    ("EU", "Pleasure", "Global"): 4,
    ("EU", "Occasional Charter", "EU"): 1,
    ("EU", "Occasional Charter", "USA"): 4,
    ("EU", "Occasional Charter", "Caribbean"): 5,
    ("EU", "Occasional Charter", "Middle East"): 3,
    ("EU", "Occasional Charter", "Asia"): 4,
    ("EU", "Occasional Charter", "Global"): 4,
    ("EU", "Commercial", "EU"): 1,
    ("EU", "Commercial", "USA"): 4,
    ("EU", "Commercial", "Caribbean"): 5,
    ("EU", "Commercial", "Middle East"): 3,
    ("EU", "Commercial", "Asia"): 4,
    ("EU", "Commercial", "Global"): 4,
    ("UK", "Pleasure", "EU"): 4,
    ("UK", "Pleasure", "USA"): 4,
    ("UK", "Pleasure", "Caribbean"): 4,
    ("UK", "Pleasure", "Middle East"): 4,
    ("UK", "Pleasure", "Asia"): 4,
    ("UK", "Pleasure", "Global"): 4,
    ("UK", "Occasional Charter", "EU"): 4,
    ("UK", "Occasional Charter", "USA"): 4,
    ("UK", "Occasional Charter", "Caribbean"): 4,
    ("UK", "Occasional Charter", "Middle East"): 4,
    ("UK", "Occasional Charter", "Asia"): 4,
    ("UK", "Occasional Charter", "Global"): 4,
    ("UK", "Commercial", "EU"): 4,
    ("UK", "Commercial", "USA"): 4,
    ("UK", "Commercial", "Caribbean"): 4,
    ("UK", "Commercial", "Middle East"): 4,
    ("UK", "Commercial", "Asia"): 4,
    ("UK", "Commercial", "Global"): 4,
    ("US", "Pleasure", "USA"): 4,
    ("US", "Pleasure", "EU"): 4,
    ("US", "Pleasure", "Caribbean"): 4,
    ("US", "Pleasure", "Middle East"): 4,
    ("US", "Pleasure", "Asia"): 4,
    ("US", "Pleasure", "Global"): 4,
    ("US", "Occasional Charter", "USA"): 3,
    ("US", "Occasional Charter", "EU"): 5,
    ("US", "Occasional Charter", "Caribbean"): 5,
    ("US", "Occasional Charter", "Middle East"): 5,
    ("US", "Occasional Charter", "Asia"): 5,
    ("US", "Occasional Charter", "Global"): 5,
    ("US", "Commercial", "USA"): 2,
    ("US", "Commercial", "EU"): 5,
    ("US", "Commercial", "Caribbean"): 5,
    ("US", "Commercial", "Middle East"): 5,
    ("US", "Commercial", "Asia"): 5,
    ("US", "Commercial", "Global"): 5,
    ("Middle East", "Pleasure", "Middle East"): 3,
    ("Middle East", "Pleasure", "EU"): 4,
    ("Middle East", "Pleasure", "Caribbean"): 5,
    ("Middle East", "Pleasure", "USA"): 4,
    ("Middle East", "Pleasure", "Asia"): 5,
    ("Middle East", "Pleasure", "Global"): 4,
    ("Middle East", "Occasional Charter", "Middle East"): 3,
    ("Middle East", "Occasional Charter", "EU"): 4,
    ("Middle East", "Occasional Charter", "Caribbean"): 5,
    ("Middle East", "Occasional Charter", "USA"): 4,
    ("Middle East", "Occasional Charter", "Asia"): 5,
    ("Middle East", "Occasional Charter", "Global"): 5,
    ("Middle East", "Commercial", "Middle East"): 3,
    ("Middle East", "Commercial", "EU"): 4,
    ("Middle East", "Commercial", "Caribbean"): 5,
    ("Middle East", "Commercial", "USA"): 4,
    ("Middle East", "Commercial", "Asia"): 5,
    ("Middle East", "Commercial", "Global"): 5,
    ("Asia", "Pleasure", "Asia"): 4,
    ("Asia", "Pleasure", "EU"): 4,
    ("Asia", "Pleasure", "Caribbean"): 5,
    ("Asia", "Pleasure", "USA"): 4,
    ("Asia", "Pleasure", "Middle East"): 4,
    ("Asia", "Pleasure", "Global"): 4,
    ("Asia", "Occasional Charter", "Asia"): 4,
    ("Asia", "Occasional Charter", "EU"): 4,
    ("Asia", "Occasional Charter", "Caribbean"): 5,
    ("Asia", "Occasional Charter", "USA"): 4,
    ("Asia", "Occasional Charter", "Middle East"): 4,
    ("Asia", "Occasional Charter", "Global"): 4,
    ("Asia", "Commercial", "Asia"): 4,
    ("Asia", "Commercial", "EU"): 4,
    ("Asia", "Commercial", "Caribbean"): 5,
    ("Asia", "Commercial", "USA"): 4,
    ("Asia", "Commercial", "Middle East"): 4,
    ("Asia", "Commercial", "Global"): 4,
    ("Other", "Pleasure", "EU"): 5,
    ("Other", "Pleasure", "USA"): 5,
    ("Other", "Pleasure", "Caribbean"): 5,
    ("Other", "Pleasure", "Middle East"): 5,
    ("Other", "Pleasure", "Asia"): 5,
    ("Other", "Pleasure", "Global"): 5,
    ("Other", "Occasional Charter", "EU"): 5,
    ("Other", "Occasional Charter", "USA"): 5,
    ("Other", "Occasional Charter", "Caribbean"): 5,
    ("Other", "Occasional Charter", "Middle East"): 5,
    ("Other", "Occasional Charter", "Asia"): 5,
    ("Other", "Occasional Charter", "Global"): 5,
    ("Other", "Commercial", "EU"): 5,
    ("Other", "Commercial", "USA"): 5,
    ("Other", "Commercial", "Caribbean"): 5,
    ("Other", "Commercial", "Middle East"): 5,
    ("Other", "Commercial", "Asia"): 5,
    ("Other", "Commercial", "Global"): 5,
}

FACTORS = [
    # (id, name, base_score, group, remark)
    ("seafarers_coc", "Acceptance of Seafarers' COC", 4, "Service & Support",
     "Flag states differ significantly in which countries' officer certificates they recognise. BVI accepts certificates from the jurisdictions listed in its Marine Circular — a carefully considered list that balances breadth with the quality assurance of vetting the issuing administrations, rather than accepting all certificates indiscriminately."),

    ("cost", "Cost", 5, "Financial",
     "Cost appears straightforward but is often more nuanced than the advertised fee suggests. Some registries offer a low headline figure but layer on annual fees, inspection fees, compliance levies, and survey charges separately. The meaningful comparison is the total five-year cost of ownership. BVI's fee structure is transparent and all-inclusive — consistently among the lowest in the industry when viewed on this basis."),

    ("psc_whitelist", "PSC Whitelist / Grey / Black", 4, "Reputation & Legal Standing",
     "The Paris MOU and Tokyo MOU publish white, grey, and black lists of flag states based on Port State Control inspection outcomes. A vessel's flag directly influences the frequency and intensity of inspections it faces in port. BVI maintains a consistent position on the Paris MOU white list, reflecting its commitment to quality shipping standards."),

    ("reputation", "Flag Reputation", 5, "Reputation & Legal Standing",
     "Beyond the quantifiable PSC regime, a flag's perceived reputation influences how port authorities, customs officials, lenders, insurers, and counterparties treat a vessel. BVI, as a British Overseas Territory flying the Red Ensign, sits within the gold-standard Red Ensign Group alongside the UK and its Overseas Territories — a status that commands genuine respect across the global maritime community."),

    ("pleasure_commercial", "Pleasure / Commercial Suitability", 5, "Commercial & Operational Framework",
     "Not all flags provide an adequate framework for commercial operations, particularly for international voyages. The USA is a clear example — well-suited for domestic pleasure registration but lacking the internationally recognised commercial regulatory framework required for charter and commercial voyages outside its waters. BVI, as part of the Red Ensign Group, operates within a fully recognised international commercial framework."),

    ("codes", "Availability of Codes", 5, "Commercial & Operational Framework",
     "The Red Ensign Group leads the industry in yacht codes — the Large Yacht Code and the Small Commercial Vessel Code set the global benchmark. BVI additionally offers the Caribbean Small Commercial Vessel Code and the Caribbean Cargo Ship Safety Code, which are particularly valuable for Caribbean operations. The REG yacht codes are widely regarded as the industry gold standard."),

    ("area_operation", "Area of Operation Alignment", 5, "Commercial & Operational Framework",
     "The codes and frameworks available under a flag should align with where the vessel actually operates. For Caribbean operations, BVI's Caribbean-specific codes provide a direct operational advantage. Flag selection and area of operation are closely interconnected decisions that should always be considered together."),

    ("yet_charter", "Specific Schemes — YET & Limited Charter", 4, "Commercial & Operational Framework",
     "BVI operates its own Yacht Exemption Tonnage (YET) scheme alongside Cayman Islands, Isle of Man, and Marshall Islands. On private yacht limited charter, BVI takes a principled position: any vessel undertaking commercial operations, even for a limited number of days per year, must meet full safety compliance standards. This reflects a commitment to the safety of crew, passengers, and the marine environment."),

    ("vat_tariff", "VAT & Tariff Considerations", 0, "Financial",
     "VAT and tariff implications are among the most significant and nuanced factors in flag selection today. The optimal flag depends on the specific combination of UBO residency, vessel use, and area of operation. BVI holds a structural advantage for non-EU owners and for EU owners operating outside EU waters, given its status as a British Overseas Territory outside the EU VAT regime."),

    ("eligibility", "Owner Eligibility", 0, "Administration & Compliance",
     "BVI's eligible jurisdiction list, updated under the Merchant Shipping (Amendment) Act 2025, is extensive — covering the EU, Commonwealth, UAE, UK, US, and many more. For owners not personally eligible, incorporating a BVI company or a company in an eligible jurisdiction provides a straightforward and well-trodden pathway, supported by BVI's world-class corporate registry infrastructure."),

    ("rep_persons", "Representative Persons", 4, "Administration & Compliance",
     "Flag registration confers nationality on a vessel, which requires a demonstrable connection to the jurisdiction for non-resident owners. BVI offers a wide choice of qualified representative persons — trust companies, legal firms, and licensed individuals — making this requirement easy to satisfy within the existing BVI ecosystem."),

    ("approachable", "Approachability of Registry", 5, "Service & Support",
     "This is a soft but meaningful factor. BVI, as a boutique registry compared to the largest flag states, offers direct access to senior management. Clients receive genuine engagement rather than navigating layers of bureaucracy. When time-sensitive situations arise, this responsiveness has real practical value."),

    ("ro_delegation", "Recognised Organisation (RO) Delegation", 4, "Service & Support",
     "BVI authorises six Recognised Organisations for statutory functions — fewer than some larger registries, but deliberately so. The Red Ensign Group maintains rigorous standards for RO approval, including periodic audits. Fewer, better-quality ROs means greater consistency in survey standards and stronger quality assurance for owners and insurers."),

    ("insurance_lender", "Insurance & Lender Premium", 5, "Financial",
     "Flag selection has a direct bearing on insurance premiums and the terms offered by marine lenders. Registries with stricter quality controls — including more rigorous RO standards — are rewarded with more favourable premium treatment. The cost savings achievable through BVI's reputation with underwriters and lenders often offset or exceed the differential in registration fees."),

    ("vessel_acceptance", "Vessel Acceptability", 4, "Administration & Compliance",
     "BVI conducts a risk assessment prior to flagging commercial and larger vessels, taking into account age, company track record, and PSC inspection history. This is not a barrier but a quality assurance measure — consistent with BVI's position as a quality flag. Owners with strong records find the process straightforward."),

    ("ease_business", "Ease of Doing Business", 5, "Service & Support",
     "Speed of service, flexibility, and helpfulness in administration are factors that only become apparent once you are working with a registry. BVI's commitment to ease of doing business is embedded in its operational culture — from initial enquiry through to ongoing vessel management."),

    ("inspections", "Inspections — Pre-Flagging & Ongoing", 4, "Administration & Compliance",
     "BVI's Flag State Inspection regime currently operates on a five-year cycle — less frequent than most comparable registries. Pre-flagging inspections are only required when the risk score assessment warrants it. For well-maintained vessels with clean records, the inspection burden is minimal."),

    ("exemptions", "Exemptions", 4, "Administration & Compliance",
     "For new builds and vessels requiring regulatory flexibility, BVI takes a pragmatic approach to exemptions — considered and reasoned rather than automatic. This reflects the BVI's philosophy of maintaining quality standards while recognising the genuine operational realities of modern yacht construction and operation."),

    ("corporate_registry", "Corporate Registry Integration", 5, "Corporate & Information",
     "BVI is one of the world's oldest and largest corporate registries, with a deeply developed ecosystem of trust companies, legal advisors, and service providers. Owners wishing to register both their owning company and their vessel in the same jurisdiction find BVI uniquely well-equipped. The motto says it best: Flag, Company, Cruise."),

    ("flag_protection", "Flag Protection & Perception", 5, "Reputation & Legal Standing",
     "As a British Overseas Territory, BVI-flagged vessels benefit from UK Royal Navy protection when required and access to British consular assistance globally. Flying the Red Ensign carries genuine weight — a signal of quality, stability, and the backing of one of the world's most respected maritime nations."),

    ("manning", "Manning Requirements", 4, "Administration & Compliance",
     "BVI's approach to manning requirements reflects the UK's pioneering work in developing yacht-specific standards and equivalencies. Practical solutions such as the largest-engine-based certification concept and dual certification pathways allow operators to meet requirements efficiently without compromising safety standards."),

    ("support_ecosystem", "Support Ecosystem", 4, "Service & Support",
     "The practical logistics of vessel management — authorised surveyors, approved service suppliers for safety equipment, life-saving appliance servicing — are materially easier within BVI's Red Ensign Group network. The broad base of UK-approved service providers means owners have access to quality support regardless of where they operate."),

    ("incentive", "Incentives for Green Shipping", 4, "Financial",
     "Incentives for green technology adoption, reduced emissions, and safe operational track records are an emerging area of flag competition. BVI does not yet offer a formal incentive programme comparable to Singapore's, but this is actively under consideration. Owner input and industry participation in shaping this programme are welcomed."),

    ("robust_law", "Robust Legal Framework", 5, "Reputation & Legal Standing",
     "BVI's maritime law is rooted in English law — one of the most thoroughly developed, internationally recognised, and commercially respected legal systems in the world. This provides owners, lenders, and insurers with certainty, predictability, and confidence in the legal standing of their vessel and its documentation."),

    ("information", "Information Availability", 4, "Corporate & Information",
     "UK-based maritime law and BVI regulations are among the most accessible, well-documented, and searchable bodies of maritime regulation in the world. This reduces administrative friction, supports legal certainty, and makes compliance management straightforward for owners and their advisors."),
]

GROUPS = [
    ("Financial", "💰"),
    ("Reputation & Legal Standing", "⚖️"),
    ("Commercial & Operational Framework", "🚢"),
    ("Administration & Compliance", "📋"),
    ("Service & Support", "🤝"),
    ("Corporate & Information", "🏛️"),
]

def get_vat_score(ubo, use, area):
    key = (ubo, use, area)
    return VAT_MATRIX.get(key, 4)

def get_eligibility_score(jurisdiction):
    if jurisdiction in ELIGIBLE_JURISDICTIONS:
        return 5
    return 3

def compute_score(profile, importances):
    total_weighted = 0
    max_weighted = 0
    factor_details = []

    vat_score = get_vat_score(profile["ubo_residency"], profile["vessel_use"], profile["cruising_area"])
    eligibility_score = get_eligibility_score(profile["jurisdiction"])

    for fid, fname, base_score, group, remark in FACTORS:
        if fid == "vat_tariff":
            bvi_score = vat_score
        elif fid == "eligibility":
            bvi_score = eligibility_score
        else:
            bvi_score = base_score

        importance = importances.get(fid, 3)
        weighted = bvi_score * importance
        max_w = 5 * importance

        total_weighted += weighted
        max_weighted += max_w
        factor_details.append({
            "id": fid, "name": fname, "group": group,
            "bvi_score": bvi_score, "importance": importance,
            "weighted": weighted, "max_weighted": max_w,
            "remark": remark,
        })

    final_score = round((total_weighted / max_weighted) * 100) if max_weighted > 0 else 0
    return final_score, factor_details

def get_verdict(score):
    if score >= 85:
        return "Excellent Fit", "#2e7d32"
    elif score >= 70:
        return "Strong Fit", "#1565c0"
    elif score >= 55:
        return "Good Fit", "#e65100"
    else:
        return "Partial Fit — Consider Carefully", "#c62828"

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "profile"
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "importances" not in st.session_state:
    st.session_state.importances = {}

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="ensign">🏴󠁧󠁢󠁥󠁮󠁧󠁿</span>
    <h1>BVI Flag Suitability Assessment</h1>
    <p class="subtitle">Personalised flag suitability analysis for yacht owners</p>
</div>
""", unsafe_allow_html=True)

# ── Step indicator ────────────────────────────────────────────────────────────
p = st.session_state.page
s1 = "done" if p in ["assessment", "report"] else ("active" if p == "profile" else "")
s2 = "done" if p == "report" else ("active" if p == "assessment" else "")
s3 = "active" if p == "report" else ""
l1 = "done" if p in ["assessment", "report"] else ""
l2 = "done" if p == "report" else ""

st.markdown(f"""
<div class="step-indicator">
    <div class="step {s1}">1</div>
    <div class="step-line {l1}"></div>
    <div class="step {s2}">2</div>
    <div class="step-line {l2}"></div>
    <div class="step {s3}">3</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — PROFILE
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "profile":

    st.markdown('<div class="section-header">Step 1 — Your Vessel Profile</div>', unsafe_allow_html=True)
    st.markdown("Answer six questions about your vessel and ownership. This shapes your personalised suitability report.")

    with st.container():
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            vessel_use = st.selectbox(
                "1. How will the vessel primarily be used?",
                ["Pleasure", "Occasional Charter", "Commercial"],
                help="Commercial includes full-time charter and cargo operations."
            )

            cruising_area = st.selectbox(
                "2. Where will the vessel mainly operate?",
                ["Caribbean", "Mediterranean", "Middle East", "USA", "Asia", "Global"],
            )

            ubo_residency = st.selectbox(
                "3. Where is the beneficial owner (UBO) based?",
                ["EU", "UK", "US", "Middle East", "Asia", "Other"],
            )

        with col2:
            ownership = st.selectbox(
                "4a. How will the yacht be owned?",
                ["Personal name", "Through a company"],
            )

            if ownership == "Personal name":
                jlabel = "4b. What is the UBO's nationality?"
            else:
                jlabel = "4b. Where is the owning company incorporated?"

            jurisdiction = st.selectbox(
                jlabel,
                ["— Select —"] + ELIGIBLE_JURISDICTIONS + ["Other (not listed)"],
            )

            vessel_stage = st.selectbox(
                "5. What stage is the vessel at?",
                ["New build", "Existing vessel, looking to re-flag", "Just researching"],
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # Eligibility note
    if jurisdiction != "— Select —":
        if jurisdiction == "Other (not listed)":
            st.markdown("""
            <div class="warning-box">
            ⚠️ <strong>Additional step required:</strong> Your current nationality / incorporation jurisdiction is not directly eligible for BVI registration. However, incorporating a BVI company or a company in an eligible jurisdiction provides a straightforward pathway — and BVI's corporate registry makes this seamless.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-box">
            ✅ <strong>{jurisdiction}</strong> is an eligible jurisdiction for direct BVI vessel registration under the Merchant Shipping (Amendment) Act, 2025.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("Continue to Assessment →", type="primary", use_container_width=True):
            if jurisdiction == "— Select —":
                st.error("Please select a nationality or incorporation jurisdiction.")
            else:
                jur = jurisdiction if jurisdiction != "Other (not listed)" else "Other (not listed)"
                st.session_state.profile = {
                    "vessel_use": vessel_use,
                    "cruising_area": cruising_area,
                    "ubo_residency": ubo_residency,
                    "ownership": ownership,
                    "jurisdiction": jur,
                    "vessel_stage": vessel_stage,
                }
                st.session_state.page = "assessment"
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — ASSESSMENT (importance sliders)
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "assessment":

    st.markdown('<div class="section-header">Step 2 — Rate Your Priorities</div>', unsafe_allow_html=True)
    st.markdown("For each factor, indicate how important it is to your flag decision. 1 = Not important, 5 = Critical.")

    importances = {}

    for group_name, group_icon in GROUPS:
        group_factors = [(fid, fname, remark) for fid, fname, _, g, remark in FACTORS if g == group_name]

        st.markdown(f'<div class="group-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="group-title">{group_icon} {group_name}</div>', unsafe_allow_html=True)

        for fid, fname, remark in group_factors:
            imp = st.slider(
                fname,
                min_value=1, max_value=5, value=3,
                key=f"imp_{fid}",
                help=remark[:120] + "..."
            )
            importances[fid] = imp

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, _ = st.columns([1, 1, 2])
    with col1:
        if st.button("← Back to Profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()
    with col2:
        if st.button("Generate Report →", type="primary", use_container_width=True):
            st.session_state.importances = importances
            st.session_state.page = "report"
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — REPORT
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "report":

    profile = st.session_state.profile
    importances = st.session_state.importances

    final_score, factor_details = compute_score(profile, importances)
    verdict, verdict_color = get_verdict(final_score)

    # ── Score hero ────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="score-hero">
        <div class="score-label">BVI Suitability Score</div>
        <div class="score-number">{final_score}</div>
        <div class="score-label">out of 100</div>
        <div class="score-verdict">{verdict}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Group scores (computed early for PDF) ────────────────────────────────
    group_scores = {}
    for g, _ in GROUPS:
        gf = [f for f in factor_details if f["group"] == g]
        if gf:
            tw = sum(f["weighted"] for f in gf)
            mw = sum(f["max_weighted"] for f in gf)
            group_scores[g] = round((tw / mw) * 100) if mw > 0 else 0

    # ── Download button ───────────────────────────────────────────────────────
    try:
        pdf_bytes = generate_pdf(profile, factor_details, final_score, group_scores)
        st.download_button(
            label="⬇  Download Full Report (PDF)",
            data=pdf_bytes,
            file_name=f"BVI_Flag_Suitability_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=False,
        )
    except Exception as e:
        st.warning(f"PDF generation unavailable: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Profile summary pills
    st.markdown("**Your profile:**", unsafe_allow_html=False)
    pills_html = "".join([
        f'<span class="pill pill-gold">{profile["vessel_use"]}</span>',
        f'<span class="pill pill-gold">{profile["cruising_area"]}</span>',
        f'<span class="pill pill-gold">UBO: {profile["ubo_residency"]}</span>',
        f'<span class="pill pill-gold">{profile["ownership"]}</span>',
        f'<span class="pill pill-gold">{profile["vessel_stage"]}</span>',
    ])
    st.markdown(pills_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Group scores chart ────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Score by Category</div>', unsafe_allow_html=True)

    fig = go.Figure(go.Bar(
        x=list(group_scores.values()),
        y=list(group_scores.keys()),
        orientation='h',
        marker=dict(
            color=list(group_scores.values()),
            colorscale=[[0, '#c0392b'], [0.4, '#e67e22'], [0.7, '#2980b9'], [1.0, '#c9a84c']],
            cmin=0, cmax=100,
        ),
        text=[f"{v}" for v in group_scores.values()],
        textposition='inside',
        textfont=dict(color='white', size=13),
    ))
    fig.update_layout(
        height=320,
        margin=dict(l=0, r=20, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[0, 100], showgrid=True, gridcolor='#eee', tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=12, family='Source Sans 3')),
        font=dict(family='Source Sans 3'),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Factor detail by group ────────────────────────────────────────────────
    st.markdown('<div class="section-header">Detailed Factor Analysis</div>', unsafe_allow_html=True)

    for group_name, group_icon in GROUPS:
        gf = [f for f in factor_details if f["group"] == group_name]
        if not gf:
            continue

        with st.expander(f"{group_icon} {group_name}", expanded=True):
            for f in gf:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{f['name']}**")
                    st.markdown(f"<span style='font-size:0.88rem;color:#555;'>{f['remark']}</span>", unsafe_allow_html=True)
                with col2:
                    stars = "⭐" * f["bvi_score"] + "☆" * (5 - f["bvi_score"])
                    st.markdown(f"**BVI Rating**<br><span style='font-size:0.9rem;'>{stars}</span>", unsafe_allow_html=True)
                with col3:
                    imp_bar = "▰" * f["importance"] + "▱" * (5 - f["importance"])
                    st.markdown(f"**Your Priority**<br><span style='color:#c9a84c;font-size:0.9rem;'>{imp_bar}</span>", unsafe_allow_html=True)
                st.markdown("---")

    # ── Special note for EU commercial in EU ─────────────────────────────────
    if profile["ubo_residency"] == "EU" and profile["vessel_use"] == "Commercial" and profile["cruising_area"] == "EU":
        st.markdown("""
        <div class="warning-box">
        <strong>Note on VAT & flag selection:</strong> For an EU-resident UBO operating commercially within EU waters, an EU flag such as Malta may offer structural VAT advantages that BVI cannot replicate. We recommend discussing your specific tax position with a maritime tax advisor before making a final decision.
        </div>
        """, unsafe_allow_html=True)

    if profile["jurisdiction"] == "Other (not listed)":
        st.markdown("""
        <div class="warning-box">
        <strong>Note on eligibility:</strong> Your nationality or incorporation jurisdiction is not directly on the BVI eligible list. Incorporating a BVI company or a company in an eligible jurisdiction resolves this — BVI's corporate registry makes this a straightforward and cost-effective step.
        </div>
        """, unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="cta-box">
        <h3>Ready to Register?</h3>
        <p style="color:rgba(255,255,255,0.8);margin:0.5rem 0 1rem 0;">
            Get in touch to discuss your specific situation, answer questions, and explore the registration process.
        </p>
        <p style="color:var(--gold-light);font-size:0.95rem;margin-bottom:0.4rem;">
            🌐 &nbsp;www.bvimaritime.vg
        </p>
        <p style="color:rgba(255,255,255,0.85);font-size:0.95rem;">
            📧 &nbsp;Jejo Joy &nbsp;·&nbsp;
            <a href="mailto:jejojoy.neelankavil@bvimaritime.vg"
               style="color:var(--gold-light);text-decoration:none;">
               jejojoy.neelankavil@bvimaritime.vg
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Yacht Certification Link ──────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:white;border:1px solid #ddd8ce;border-radius:12px;padding:1.5rem 2rem;
                box-shadow:0 2px 8px rgba(13,33,55,0.06);text-align:center;">
        <div style="font-family:'Playfair Display',serif;font-size:1.1rem;color:#0d2137;margin-bottom:0.5rem;">
            🧾 &nbsp;Want to know what statutory certificates are required for your yacht?
        </div>
        <p style="color:#555;font-size:0.92rem;margin-bottom:1rem;">
            Check our dedicated Yacht Certification tool — enter your vessel details and get a complete picture of the certificates you need.
        </p>
        <a href="https://yachtcertification.streamlit.app/" target="_blank"
           style="background:#0d2137;color:#e8c97a;padding:0.6rem 1.8rem;border-radius:6px;
                  text-decoration:none;font-weight:600;font-size:0.95rem;letter-spacing:0.03em;">
            Open Yacht Certification Tool →
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, _ = st.columns([1, 1, 2])
    with col1:
        if st.button("← Adjust Priorities", use_container_width=True):
            st.session_state.page = "assessment"
            st.rerun()
    with col2:
        if st.button("Start Over", use_container_width=True):
            st.session_state.page = "profile"
            st.session_state.profile = {}
            st.session_state.importances = {}
            st.rerun()

    # ── About the Developer ───────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#f0ede6;border-radius:12px;padding:2rem 2.5rem;margin-top:1rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.2rem;color:#0d2137;
                    border-left:4px solid #c9a84c;padding-left:1rem;margin-bottom:1.2rem;">
            About the Developer
        </div>
        <p style="color:#2c3e50;font-size:0.95rem;line-height:1.8;margin-bottom:1rem;">
            Jejo Joy started his career the way most maritime professionals do — on the ships themselves,
            and then in the survey rooms of classification societies, standing at the intersection of
            steel, sea, and regulation. Over the years, that vantage point expanded: Flag State,
            Port State Control, newbuilding supervision, dry-docking, ISM, ISPS, MLC — the full
            arc of what it means to keep a vessel compliant, safe, and seaworthy.
        </p>
        <p style="color:#2c3e50;font-size:0.95rem;line-height:1.8;margin-bottom:1rem;">
            Now, as a Naval Architect and Maritime Professional at the British Virgin Islands
            Ship Registry, that experience finds its purpose in a different way —
            helping owners, operators, and advisors navigate one of the most consequential decisions
            in yacht ownership: the choice of flag.
        </p>
        <p style="color:#2c3e50;font-size:0.95rem;line-height:1.8;margin-bottom:1.5rem;">
            This tool is the result of a conviction that maritime expertise and modern technology
            should work together — that the knowledge built up over decades at sea, in shipyards,
            and in registry offices can be made accessible, structured, and useful to anyone facing
            a complex decision. There is more to come.
        </p>
        <a href="https://www.linkedin.com/in/jejo-j-b324a7a7/" target="_blank"
           style="display:inline-flex;align-items:center;gap:0.5rem;
                  background:#0d2137;color:#e8c97a;padding:0.55rem 1.4rem;
                  border-radius:6px;text-decoration:none;font-weight:600;font-size:0.9rem;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#e8c97a" viewBox="0 0 24 24">
              <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239
                       5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966
                       0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783
                       1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4
                       0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
            </svg>
            Connect on LinkedIn
        </a>
    </div>
    """, unsafe_allow_html=True)
