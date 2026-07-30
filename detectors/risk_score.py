SEVERITY_SCORE = {
    "LOW": 20,
    "MEDIUM": 50,
    "HIGH": 80,
    "CRITICAL": 100
}


def calculate_risk(severity):

    return SEVERITY_SCORE.get(
        severity,
        0
    )