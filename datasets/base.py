from abc import ABC, abstractmethod
from typing import List, Dict


class BaseDataset(ABC):
    """
    Abstract base class for all disaster datasets.
    Every dataset must implement the load() method.
    """

    def __init__(self, data_root: str, subset: str):
        """
        Args:
            data_root: Path to the root directory of the dataset
            subset: Which subset/task to load (e.g. 'bearing_body', 'caption')
        """
        self.data_root = data_root
        self.subset = subset
        self.data = []

    @abstractmethod
    def load(self) -> List[Dict]:
        """
        Load and return the dataset samples.

        Returns:
            List of dicts, each containing at minimum:
                - 'id': unique sample identifier
                - 'image_path' or 'pre_image_path'/'post_image_path': path(s) to image(s)
                - 'question': the text prompt
                - 'answer': the ground truth answer
        """
        raise NotImplementedError

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]