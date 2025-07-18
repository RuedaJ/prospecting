# modules/score.py

def score_lead(lead: dict) -> int:
    """
    Compute a lead score from available enriched data and segment.

    Parameters:
        lead (dict): A dictionary or row with keys:
            - 'Enriched Email'
            - 'LinkedIn'
            - 'Title'
            - 'Segment'

    Returns:
        int: Total lead score
    """
    score = 0

    # Email presence = 10 pts
    if lead.get("Enriched Email") and "@" in lead["Enriched Email"]:
        score += 10

    # LinkedIn presence = 5 pts
    if lead.get("LinkedIn") and "linkedin.com" in lead["LinkedIn"]:
        score += 5

    # Executive title = 5 pts
    if lead.get("Title") and "executive" in lead["Title"].lower():
        score += 5

    # Strategic segment = 10 pts
    if lead.get("Segment") in ["Old Money / HNW Individuals", "Diplomatic / Embassy"]:
        score += 10

    return score
# Lead scoring logic based on defined weights
