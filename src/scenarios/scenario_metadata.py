import csv
from pathlib import Path


METADATA_COLUMNS = [
    "scenario_id",
    "person_id",
    "source_image",
    "output_image",
    "lighting",
    "camera",
    "pose",
    "blur",
    "noise",
    "quality",
    "skin_tone",
    "age",
    "random_seed",
]


def write_scenario_metadata(
    records,
    output_path,
    random_seed
):
    """
    Write scenario generation metadata to CSV.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=METADATA_COLUMNS
        )

        writer.writeheader()

        for record in records:

            conditions = record.get(
                "conditions",
                {}
            )

            writer.writerow({
                "scenario_id": record.get(
                    "scenario_id",
                    ""
                ),

                "person_id": record.get(
                    "person_id",
                    ""
                ),

                "source_image": record.get(
                    "source_image",
                    ""
                ),

                "output_image": record.get(
                    "output_image",
                    ""
                ),

                "lighting": conditions.get(
                    "lighting",
                    ""
                ),

                "camera": conditions.get(
                    "camera",
                    ""
                ),

                "pose": conditions.get(
                    "pose",
                    ""
                ),

                "blur": conditions.get(
                    "blur",
                    ""
                ),

                "noise": conditions.get(
                    "noise",
                    ""
                ),

                "quality": conditions.get(
                    "quality",
                    ""
                ),

                "skin_tone": conditions.get(
                    "skin_tone",
                    ""
                ),

                "age": conditions.get(
                    "age",
                    ""
                ),

                "random_seed": random_seed,
            })

    print(
        f"Scenario metadata written to "
        f"{output_path}"
    )