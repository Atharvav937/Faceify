from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import numpy as np


@dataclass
class GenerationContext:
    """
    Holds the state of one synthetic image generation operation.
    """

    source_image: np.ndarray
    current_image: Optional[np.ndarray] = None

    source_filename: str = ""

    parameters: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.current_image is None:
            self.current_image = self.source_image.copy()

    def reset(self):
        """Reset current image back to the original source image."""
        self.current_image = self.source_image.copy()

    def update_image(self, image: np.ndarray):
        """Update the current generated image."""
        self.current_image = image