import random

from config import (
    LIGHTING_PRESETS,
    CAMERA_ANGLE_PRESETS,
    POSE_PRESETS,
    BLUR_LEVELS,
    NOISE_LEVELS,
    QUALITY_LEVELS,
    SKIN_TONE_LEVELS,
    AGE_LEVELS,
)


# ============================================================
# SCENARIO CONFIGURATION
# ============================================================

SCENARIO_COUNT = 10

# Fixed seed makes dataset generation reproducible.
# Same seed + same configuration = same scenarios.
RANDOM_SEED = 42


# Number of conditions applied in a scenario.
#
# Example:
# 3 conditions:
# lighting + camera + quality
#
# 5 conditions:
# lighting + camera + pose + skin tone + quality
#
MIN_CONDITIONS = 3
MAX_CONDITIONS = 5


# Available condition categories
CONDITION_CATEGORIES = [
    "lighting",
    "camera",
    "pose",
    "blur",
    "noise",
    "quality",
    "skin_tone",
    "age",
]


def get_random_variation(condition, rng):
    """
    Select one variation from a condition.
    """

    if condition == "lighting":
        return rng.choice(
            list(LIGHTING_PRESETS.keys())
        )

    if condition == "camera":
        return rng.choice(
            list(CAMERA_ANGLE_PRESETS.keys())
        )

    if condition == "pose":
        return rng.choice(
            list(POSE_PRESETS.keys())
        )

    if condition == "blur":
        return rng.choice(
            list(BLUR_LEVELS.keys())
        )

    if condition == "noise":
        return rng.choice(
            list(NOISE_LEVELS.keys())
        )

    if condition == "quality":
        return rng.choice(
            list(QUALITY_LEVELS.keys())
        )

    if condition == "skin_tone":
        return rng.choice(
            list(SKIN_TONE_LEVELS.keys())
        )

    if condition == "age":
        return rng.choice(
            list(AGE_LEVELS.keys())
        )

    raise ValueError(
        f"Unknown condition: {condition}"
    )


def generate_scenarios(
    count=SCENARIO_COUNT,
    seed=RANDOM_SEED
):
    """
    Generate controlled random scenario definitions.

    Returns a list such as:

    [
        {
            "scenario_id": "scenario_0001",
            "conditions": {
                "lighting": "left_soft_warm",
                "camera": "slight_left",
                "quality": "low"
            }
        }
    ]
    """

    rng = random.Random(seed)

    scenarios = []

    for index in range(1, count + 1):

        condition_count = rng.randint(
            MIN_CONDITIONS,
            MAX_CONDITIONS
        )

        selected_conditions = rng.sample(
            CONDITION_CATEGORIES,
            condition_count
        )

        conditions = {}

        for condition in selected_conditions:

            variation = get_random_variation(
                condition,
                rng
            )

            conditions[condition] = variation

        scenario = {
            "scenario_id": (
                f"scenario_{index:04d}"
            ),
            "conditions": conditions
        }

        scenarios.append(scenario)

    return scenarios


def print_scenarios(scenarios):
    """
    Print generated scenarios in a readable format.
    """

    print()
    print("=" * 70)
    print("GENERATED SCENARIOS")
    print("=" * 70)

    for scenario in scenarios:

        print(
            f"\n{scenario['scenario_id']}"
        )

        for condition, variation in scenario[
            "conditions"
        ].items():

            print(
                f"  {condition}: {variation}"
            )

    print()
    print("=" * 70)