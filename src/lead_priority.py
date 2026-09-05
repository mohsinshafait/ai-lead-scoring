def get_priority(probability):
    """
    Convert conversion probability into a business priority.
    """

    if probability >= 0.70:
        return "High"

    elif probability >= 0.40:
        return "Medium"

    else:
        return "Low"


def get_recommended_action(priority):
    """
    Recommend a sales action based on lead priority.
    """

    if priority == "High":
        return "Contact immediately"

    elif priority == "Medium":
        return "Follow up within 24 hours"

    else:
        return "Nurture and monitor"