from src.lead_priority import (
    get_priority,
    get_recommended_action
)


test_probabilities = [
    0.82,
    0.65,
    0.45,
    0.32,
    0.18
]


for probability in test_probabilities:

    priority = get_priority(probability)

    action = get_recommended_action(priority)

    print(
        f"Probability: {probability:.0%} | "
        f"Priority: {priority} | "
        f"Action: {action}"
    )