import os
import csv
from pathlib import Path

from config import (
    INPUT_FOLDER,
    OUTPUT_FOLDER,
    METADATA_PATH,
    OVERWRITE_EXISTING,
    LIGHTING_PRESETS,
    CAMERA_ANGLE_PRESETS,
    POSE_PRESETS,
    BLUR_LEVELS,
    NOISE_LEVELS,
    QUALITY_LEVELS,
    SKIN_TONE_LEVELS,
    AGE_LEVELS,
)

from utils.image_io import read_image, save_image

from modules.lighting import apply_lighting
from modules.camera_angle import apply_camera_angle
from modules.pose import apply_pose
from modules.blur import apply_gaussian_blur
from modules.noise import add_gaussian_noise
from modules.quality import apply_jpeg_compression
from modules.skin_tone import adjust_skin_tone
from modules.age import apply_age


class SyntheticImageGenerator:

    def __init__(self):

        self.input_folder = Path(INPUT_FOLDER)
        self.output_folder = Path(OUTPUT_FOLDER)
        self.metadata_path = Path(METADATA_PATH)

        self.metadata_records = []

    # ============================================================
    # MAIN RUNNER
    # ============================================================

    def run(self):

        self._prepare_output_directory()

        image_files = self._get_input_images()

        if not image_files:
            print("No images found in input folder.")
            return

        for image_file in image_files:
            self.process_image(image_file)

        self._write_metadata()

    # ============================================================
    # PROCESS IMAGE
    # ============================================================

    def process_image(self, image_file):

        input_path = self.input_folder / image_file

        image = read_image(str(input_path))

        if image is None:
            print(f"Failed to read image: {image_file}")
            return

        base_name = input_path.stem
        ext = input_path.suffix

        # --------------------------------------------------------
        # Create person folder
        # --------------------------------------------------------

        person_folder = self.output_folder / base_name

        person_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        # --------------------------------------------------------
        # 1. Lighting
        # --------------------------------------------------------

        self._generate_lighting_variations(
            image,
            image_file,
            base_name,
            ext,
            person_folder
        )

        # --------------------------------------------------------
        # 2. Camera Angle
        # --------------------------------------------------------

        self._generate_camera_angle_variations(
            image,
            image_file,
            base_name,
            ext,
            person_folder
        )

        # --------------------------------------------------------
        # 3. Pose
        # --------------------------------------------------------

        self._generate_pose_variations(
            image,
            image_file,
            base_name,
            ext,
            person_folder
        )

        # --------------------------------------------------------
        # 4. Blur
        # --------------------------------------------------------

        self._generate_blur_variations(
            image,
            image_file,
            base_name,
            ext,
            person_folder
        )

        # --------------------------------------------------------
        # 5. Noise
        # --------------------------------------------------------

        self._generate_noise_variations(
            image,
            image_file,
            base_name,
            ext,
            person_folder
        )

        # --------------------------------------------------------
        # 6. Quality
        # --------------------------------------------------------

        self._generate_quality_variations(
            image,
            image_file,
            base_name,
            ext,
            person_folder
        )

        # --------------------------------------------------------
        # 7. Skin Tone
        # --------------------------------------------------------

        self._generate_skin_tone_variations(
            image,
            image_file,
            base_name,
            ext,
            person_folder
        )

        # --------------------------------------------------------
        # 8. Age
        # --------------------------------------------------------

        self._generate_age_variations(
            image,
            image_file,
            base_name,
            ext,
            person_folder
        )

        print(
            f"{image_file} processed successfully."
        )

    # ============================================================
    # LIGHTING
    # ============================================================

    def _generate_lighting_variations(
        self,
        image,
        image_file,
        base_name,
        ext,
        person_folder
    ):

        output_folder = person_folder / "lighting"

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        for preset_name, params in LIGHTING_PRESETS.items():

            filename = f"{preset_name}{ext}"

            output_path = output_folder / filename

            self._add_metadata(
                base_name,
                image_file,
                output_path,
                "lighting",
                preset_name,
                (
                    f"direction={params['direction']};"
                    f"hardness={params['hardness']};"
                    f"temperature={params['temperature']};"
                    f"exposure={params['exposure']};"
                    f"intensity={params['intensity']}"
                )
            )

            if output_path.exists() and not OVERWRITE_EXISTING:
                continue

            output_image = apply_lighting(
                image,
                direction=params["direction"],
                hardness=params["hardness"],
                temperature=params["temperature"],
                exposure=params["exposure"],
                intensity=params["intensity"]
            )

            save_image(
                str(output_path),
                output_image
            )

    # ============================================================
    # CAMERA ANGLE
    # ============================================================

    def _generate_camera_angle_variations(
        self,
        image,
        image_file,
        base_name,
        ext,
        person_folder
    ):

        output_folder = person_folder / "camera"

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        for angle_name, params in CAMERA_ANGLE_PRESETS.items():

            filename = f"{angle_name}{ext}"

            output_path = output_folder / filename

            self._add_metadata(
                base_name,
                image_file,
                output_path,
                "camera_angle",
                angle_name,
                f"strength={params['strength']}"
            )

            if output_path.exists() and not OVERWRITE_EXISTING:
                continue

            output_image = apply_camera_angle(
                image,
                angle=angle_name,
                strength=params["strength"]
            )

            save_image(
                str(output_path),
                output_image
            )

    # ============================================================
    # POSE
    # ============================================================

    def _generate_pose_variations(
        self,
        image,
        image_file,
        base_name,
        ext,
        person_folder
    ):

        output_folder = person_folder / "pose"

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        for pose_name, params in POSE_PRESETS.items():

            filename = f"{pose_name}{ext}"

            output_path = output_folder / filename

            self._add_metadata(
                base_name,
                image_file,
                output_path,
                "pose",
                pose_name,
                f"strength={params['strength']}"
            )

            if output_path.exists() and not OVERWRITE_EXISTING:
                continue

            output_image = apply_pose(
                image,
                pose=pose_name,
                strength=params["strength"]
            )

            save_image(
                str(output_path),
                output_image
            )

    # ============================================================
    # BLUR
    # ============================================================

    def _generate_blur_variations(
        self,
        image,
        image_file,
        base_name,
        ext,
        person_folder
    ):

        output_folder = person_folder / "blur"

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        for level_name, params in BLUR_LEVELS.items():

            filename = f"{level_name}{ext}"

            output_path = output_folder / filename

            self._add_metadata(
                base_name,
                image_file,
                output_path,
                "blur",
                level_name,
                (
                    f"kernel={params['kernel_size']};"
                    f"sigma={params['sigma']}"
                )
            )

            if output_path.exists() and not OVERWRITE_EXISTING:
                continue

            output_image = apply_gaussian_blur(
                image,
                params["kernel_size"],
                params["sigma"]
            )

            save_image(
                str(output_path),
                output_image
            )

    # ============================================================
    # NOISE
    # ============================================================

    def _generate_noise_variations(
        self,
        image,
        image_file,
        base_name,
        ext,
        person_folder
    ):

        output_folder = person_folder / "noise"

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        for level_name, std_dev in NOISE_LEVELS.items():

            filename = f"{level_name}{ext}"

            output_path = output_folder / filename

            self._add_metadata(
                base_name,
                image_file,
                output_path,
                "noise",
                level_name,
                str(std_dev)
            )

            if output_path.exists() and not OVERWRITE_EXISTING:
                continue

            output_image = add_gaussian_noise(
                image,
                std_dev
            )

            save_image(
                str(output_path),
                output_image
            )

    # ============================================================
    # QUALITY
    # ============================================================

    def _generate_quality_variations(
        self,
        image,
        image_file,
        base_name,
        ext,
        person_folder
    ):

        output_folder = person_folder / "quality"

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        for level_name, quality_value in QUALITY_LEVELS.items():

            filename = f"{level_name}{ext}"

            output_path = output_folder / filename

            self._add_metadata(
                base_name,
                image_file,
                output_path,
                "quality",
                level_name,
                str(quality_value)
            )

            if output_path.exists() and not OVERWRITE_EXISTING:
                continue

            output_image = apply_jpeg_compression(
                image,
                quality_value
            )

            save_image(
                str(output_path),
                output_image
            )

    # ============================================================
    # SKIN TONE
    # ============================================================

    def _generate_skin_tone_variations(
        self,
        image,
        image_file,
        base_name,
        ext,
        person_folder
    ):

        output_folder = person_folder / "skin_tone"

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        for level_name, params in SKIN_TONE_LEVELS.items():

            filename = f"{level_name}{ext}"

            output_path = output_folder / filename

            self._add_metadata(
                base_name,
                image_file,
                output_path,
                "skin_tone",
                level_name,
                (
                    f"y_scale={params['y_scale']};"
                    f"y_offset={params['y_offset']};"
                    f"cr_shift={params['cr_shift']};"
                    f"cb_shift={params['cb_shift']}"
                )
            )

            if output_path.exists() and not OVERWRITE_EXISTING:
                continue

            output_image = adjust_skin_tone(
                image,
                params["y_scale"],
                params["y_offset"],
                params["cr_shift"],
                params["cb_shift"]
            )

            save_image(
                str(output_path),
                output_image
            )

    # ============================================================
    # AGE
    # ============================================================

    def _generate_age_variations(
        self,
        image,
        image_file,
        base_name,
        ext,
        person_folder
    ):

        output_folder = person_folder / "age"

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        for age_name, params in AGE_LEVELS.items():

            filename = f"{age_name}{ext}"

            output_path = output_folder / filename

            self._add_metadata(
                base_name,
                image_file,
                output_path,
                "age",
                age_name,
                params["description"]
            )

            if output_path.exists() and not OVERWRITE_EXISTING:
                continue

            output_image = apply_age(
                image,
                age_level=age_name
            )

            save_image(
                str(output_path),
                output_image
            )

    # ============================================================
    # METADATA
    # ============================================================

    def _add_metadata(
        self,
        person_id,
        original_image,
        output_path,
        condition,
        variation,
        value
    ):

        self.metadata_records.append({
            "person_id": person_id,
            "original_image": original_image,
            "output_path": str(output_path),
            "condition": condition,
            "variation": variation,
            "value": value
        })

    def _write_metadata(self):

        self.metadata_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.metadata_path,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as f:

            fieldnames = [
                "person_id",
                "original_image",
                "output_path",
                "condition",
                "variation",
                "value"
            ]

            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(self.metadata_records)

        print(
            f"Metadata manifest written to "
            f"{self.metadata_path}"
        )

    # ============================================================
    # HELPERS
    # ============================================================

    def _prepare_output_directory(self):

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    def _get_input_images(self):

        return [
            file
            for file in os.listdir(self.input_folder)
            if file.lower().endswith(
                (".jpg", ".jpeg", ".png")
            )
        ]