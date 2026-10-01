from pathlib import Path

from config import (
    LIGHTING_PRESETS,
    CAMERA_ANGLE_PRESETS,
    POSE_PRESETS,
    BLUR_LEVELS,
    NOISE_LEVELS,
    QUALITY_LEVELS,
    SKIN_TONE_LEVELS,
    AGE_LEVELS,
    OVERWRITE_EXISTING,
)

from utils.image_io import save_image

from modules.lighting import apply_lighting
from modules.camera_angle import apply_camera_angle
from modules.pose import apply_pose
from modules.blur import apply_gaussian_blur
from modules.noise import add_gaussian_noise
from modules.quality import apply_jpeg_compression
from modules.skin_tone import adjust_skin_tone
from modules.age import apply_age

from scenarios.scenario_config import generate_scenarios


class ScenarioGenerator:

    def __init__(
        self,
        output_folder,
        scenario_count=10,
        random_seed=42
    ):
        self.output_folder = Path(output_folder)
        self.scenario_count = scenario_count
        self.random_seed = random_seed

    # ============================================================
    # GENERATE SCENARIOS FOR ONE IMAGE
    # ============================================================

    def generate_for_image(
        self,
        image,
        person_id,
        extension=".jpg"
    ):
        person_folder = (
            self.output_folder /
            person_id
        )

        scenario_folder = (
            person_folder /
            "scenarios"
        )

        scenario_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        scenarios = generate_scenarios(
            count=self.scenario_count,
            seed=self.random_seed
        )

        generated_records = []

        for scenario in scenarios:

            scenario_id = scenario["scenario_id"]

            conditions = scenario["conditions"]

            output_filename = (
                f"{scenario_id}{extension}"
            )

            output_path = (
                scenario_folder /
                output_filename
            )

            # ----------------------------------------------------
            # If file already exists
            # ----------------------------------------------------

            if (
                output_path.exists()
                and not OVERWRITE_EXISTING
            ):
                generated_records.append(
                    {
                        "scenario_id": scenario_id,
                        "person_id": person_id,
                        "source_image": (
                            f"{person_id}{extension}"
                        ),
                        "output_image": output_filename,
                        "output_path": str(
                            output_path
                        ),
                        "conditions": conditions,
                    }
                )

                continue

            # ----------------------------------------------------
            # Apply scenario
            # ----------------------------------------------------

            generated_image = self._apply_conditions(
                image,
                conditions
            )

            # ----------------------------------------------------
            # Save image
            # ----------------------------------------------------

            save_image(
                str(output_path),
                generated_image
            )

            # ----------------------------------------------------
            # Store metadata record
            # ----------------------------------------------------

            generated_records.append(
                {
                    "scenario_id": scenario_id,

                    "person_id": person_id,

                    "source_image": (
                        f"{person_id}{extension}"
                    ),

                    "output_image": output_filename,

                    "output_path": str(
                        output_path
                    ),

                    "conditions": conditions,
                }
            )

            print(
                f"Generated {person_id} / "
                f"{scenario_id}"
            )

        return generated_records

    # ============================================================
    # APPLY ALL SCENARIO CONDITIONS
    # ============================================================

    def _apply_conditions(
        self,
        image,
        conditions
    ):
        result = image.copy()

        # ========================================================
        # 1. CAMERA
        # ========================================================

        if "camera" in conditions:

            camera_name = conditions["camera"]

            params = CAMERA_ANGLE_PRESETS[
                camera_name
            ]

            result = apply_camera_angle(
                result,
                angle=camera_name,
                strength=params["strength"]
            )

        # ========================================================
        # 2. POSE
        # ========================================================

        if "pose" in conditions:

            pose_name = conditions["pose"]

            params = POSE_PRESETS[
                pose_name
            ]

            result = apply_pose(
                result,
                pose=pose_name,
                strength=params["strength"]
            )

        # ========================================================
        # 3. LIGHTING
        # ========================================================

        if "lighting" in conditions:

            lighting_name = conditions[
                "lighting"
            ]

            params = LIGHTING_PRESETS[
                lighting_name
            ]

            result = apply_lighting(
                result,

                direction=params[
                    "direction"
                ],

                hardness=params[
                    "hardness"
                ],

                temperature=params[
                    "temperature"
                ],

                exposure=params[
                    "exposure"
                ],

                intensity=params[
                    "intensity"
                ]
            )

        # ========================================================
        # 4. SKIN TONE
        # ========================================================

        if "skin_tone" in conditions:

            skin_name = conditions[
                "skin_tone"
            ]

            params = SKIN_TONE_LEVELS[
                skin_name
            ]

            result = adjust_skin_tone(
                result,

                params["y_scale"],

                params["y_offset"],

                params["cr_shift"],

                params["cb_shift"]
            )

        # ========================================================
        # 5. AGE
        # ========================================================

        if "age" in conditions:

            age_name = conditions["age"]

            result = apply_age(
                result,
                age_level=age_name
            )

        # ========================================================
        # 6. BLUR
        # ========================================================

        if "blur" in conditions:

            blur_name = conditions["blur"]

            params = BLUR_LEVELS[
                blur_name
            ]

            result = apply_gaussian_blur(
                result,

                params["kernel_size"],

                params["sigma"]
            )

        # ========================================================
        # 7. NOISE
        # ========================================================

        if "noise" in conditions:

            noise_name = conditions[
                "noise"
            ]

            std_dev = NOISE_LEVELS[
                noise_name
            ]

            result = add_gaussian_noise(
                result,
                std_dev
            )

        # ========================================================
        # 8. QUALITY
        # ========================================================

        if "quality" in conditions:

            quality_name = conditions[
                "quality"
            ]

            quality_value = QUALITY_LEVELS[
                quality_name
            ]

            result = apply_jpeg_compression(
                result,
                quality_value
            )

        return result