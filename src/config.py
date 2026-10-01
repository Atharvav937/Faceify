from pathlib import Path

OVERWRITE_EXISTING = False

# Project root (one level above src)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FOLDER = PROJECT_ROOT / "data" / "input"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "output"
OUTPUT_IMAGES_FOLDER = OUTPUT_FOLDER / "images"
METADATA_PATH = OUTPUT_FOLDER / "metadata.csv"


LIGHTING_LEVELS = {
    "very_dark": -80,
    "dark": -40,
    "normal": 0,
    "bright": 40,
    "very_bright": 80
}


BLUR_LEVELS = {
    "light": {
        "kernel_size": (5, 5),
        "sigma": 0
    },
    "medium": {
        "kernel_size": (11, 11),
        "sigma": 0
    }
}


NOISE_LEVELS = {
    "light": 10,
    "medium": 25
}


QUALITY_LEVELS = {
    "high": 90,
    "medium": 60,
    "low": 30
}


SKIN_TONE_LEVELS = {
    "pale": {
        "y_scale": 1.2,
        "y_offset": 15,
        "cr_shift": -5,
        "cb_shift": 5
    },
    "fair": {
        "y_scale": 1.0,
        "y_offset": 0,
        "cr_shift": 0,
        "cb_shift": 0
    },
    "light_brown": {
        "y_scale": 0.75,
        "y_offset": -10,
        "cr_shift": 5,
        "cb_shift": -5
    },
    "dark_brown": {
        "y_scale": 0.5,
        "y_offset": -20,
        "cr_shift": 10,
        "cb_shift": -10
    }
}


# Skin detection color space ranges and processing thresholds
YCRCB_RANGE = {
    "y_min": 40,
    "y_max": 255,
    "cr_min": 133,
    "cr_max": 175,
    "cb_min": 80,
    "cb_max": 135
}


HSV_RANGE = {
    "h_min": 0,
    "h_max": 22,
    "s_min": 18,
    "s_max": 170,
    "v_min": 40,
    "v_max": 255
}


MORPH_CLOSE_KERNEL_SIZE = 31
MORPH_OPEN_KERNEL_SIZE = 3
GAUSSIAN_KERNEL_SIZE = 15


# ============================================================
# ADVANCED LIGHTING PRESETS
# ============================================================

LIGHTING_PRESETS = {
    "front_soft_neutral": {
        "direction": "front",
        "hardness": "soft",
        "temperature": "neutral",
        "exposure": 0.0,
        "intensity": 0.25
    },

    "left_soft_warm": {
        "direction": "left",
        "hardness": "soft",
        "temperature": "warm",
        "exposure": 0.1,
        "intensity": 0.35
    },

    "right_soft_cool": {
        "direction": "right",
        "hardness": "soft",
        "temperature": "cool",
        "exposure": 0.1,
        "intensity": 0.35
    },

    "left_hard_neutral": {
        "direction": "left",
        "hardness": "hard",
        "temperature": "neutral",
        "exposure": 0.0,
        "intensity": 0.45
    },

    "right_hard_warm": {
        "direction": "right",
        "hardness": "hard",
        "temperature": "warm",
        "exposure": -0.1,
        "intensity": 0.45
    },

    "top_soft_neutral": {
        "direction": "top",
        "hardness": "soft",
        "temperature": "neutral",
        "exposure": 0.0,
        "intensity": 0.35
    },

    "bottom_soft_cool": {
        "direction": "bottom",
        "hardness": "soft",
        "temperature": "cool",
        "exposure": -0.1,
        "intensity": 0.30
    }
}

# ============================================================
# CAMERA ANGLE PRESETS
# ============================================================

CAMERA_ANGLE_PRESETS = {
    "frontal": {
        "strength": 0.00
    },

    "slight_left": {
        "strength": 0.08
    },

    "slight_right": {
        "strength": 0.08
    },

    "left": {
        "strength": 0.14
    },

    "right": {
        "strength": 0.14
    }
}

# ============================================================
# POSE PRESETS
# ============================================================

POSE_PRESETS = {
    "frontal": {
        "strength": 0.00
    },

    "tilt_left": {
        "strength": 0.50
    },

    "tilt_right": {
        "strength": 0.50
    },

    "tilt_up": {
        "strength": 0.35
    },

    "tilt_down": {
        "strength": 0.35
    }
}



# ============================================================
# AGE PRESETS
# ============================================================

AGE_LEVELS = {
    "young": {
        "description": "smooth youthful appearance"
    },

    "adult": {
        "description": "neutral adult appearance"
    },

    "older": {
        "description": "enhanced texture and local contrast"
    }
}