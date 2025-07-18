# modules/enrich.py

def enrich_contact(name: str, company: str) -> dict:
    """
    Simulated enrichment from an API (like Clearbit).
    Replace this logic with real API calls if needed.
    """
    try:
        if not name or not company:
            return {}

        email = f"{name.split()[0].lower()}@{company.lower().replace(' ', '')}.com"
        title = "CEO" if "founder" in company.lower() else "Executive"
        linkedin = f"https://www.linkedin.com/in/{name.replace(' ', '').lower()}"
        logo = f"https://logo.clearbit.com/{company.lower().replace(' ', '')}.com"

        return {
            "email": email,
            "title": title,
            "linkedin": linkedin,
            "logo": logo
        }
    except Exception as e:
        return {
            "error": str(e)
        }
# Contact enrichment logic using API
