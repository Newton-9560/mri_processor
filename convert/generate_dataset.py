import random
import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt
from tqdm import tqdm
from .utils import get_name, get_slice

t1w = ['./anat/sub-CC00054XX05_ses-8800_T1w.nii.gz',
       './anat/sub-CC00054XX05_ses-8800_desc-restore_T1w.nii.gz']
root = './t1w&t2w/'


class DatasetGenerator:
    def __init__(self, source_root, get_t2w_path_from_t1w):
        """
        A class to generate datasets from T1-weighted and T2-weighted MRI images.

        :param source_root: Directory containing the source MRI files.
        :param get_t2w_path_from_t1w: Function to derive the path of a T2-weighted image given a T1-weighted image path.
        """

        self.source_root = source_root
        self.get_t2w_path = get_t2w_path_from_t1w

    def get_path(self, file_name):
        """
        Constructs the full path for a file within the source directory.

        :param file_name: The name of the file.
        :return: Full path of the file.
        """
        return os.path.join(self.source_root, file_name)

    def file_preprocess(self, convert_name, file_type=0):
        """
        Renames files based on a conversion function and file type.

        :param convert_name: Function to generate the new name for the file.
        :param file_type: Indicates the type of MRI file (0 for T1w, 1 for T2w).
        """
        t = ['T1w', 'T2w'][file_type]
        for f in os.listdir(self.source_root):
            if t in f:
                os.rename(self.get_path(f), convert_name(self.get_path(f)))

    def get_t1w_path(self, ignore_unpaired=True, ratio=0.8, shuffle=True):
        """
        Populates the list of T1-weighted image paths that have corresponding T2-weighted images.

        :param shuffle: shuffle the data or not
        :param ratio: the ratio of the training dataset and test dataset
        :param ignore_unpaired: If True, ignores T1w images without a corresponding T2w image.
        """
        t1w_path = []
        for f in os.listdir(self.source_root):
            if 'T1w' in f and os.path.exists(self.get_path(self.get_t2w_path(f))):
                t1w_path.append(self.get_path(f))

        if shuffle:
            random.shuffle(t1w_path)
        if 0 < ratio < 1:
            split_index = int(len(t1w_path) * ratio)
            return t1w_path[:split_index], t1w_path[split_index:]
        else:
            return t1w_path

    def generate_dataset(self, t1w_path, dataset_root, directions=None,
                         preserving_ratio=0.4):
        """
        Generates and saves slices from T1w and T2w images as individual PNG files.

        :param dataset_root: Directory to save the generated dataset.
        :param directions: List of directions (axes) along which to slice the images. Defaults to [0, 1, 2].
        :param preserving_ratio: The minimum ratio of non-zero pixels in a slice for it to be saved.
        """

        if directions is None:
            directions = [0, 1, 2]

        if not os.path.exists(dataset_root):
            os.makedirs(dataset_root)
            os.mkdir(dataset_root + 't1w')
            os.mkdir(dataset_root + 't2w')
            print("Create new dataset in {}".format(dataset_root))
        else:
            print("Add data into existing folder {}".format(dataset_root))

        count = 0
        for direction in directions:
            for t1w_nii_path in t1w_path:
                img_t1w = nib.load(t1w_nii_path)
                img_t2w = nib.load(self.get_t2w_path(t1w_nii_path))
                if img_t2w.shape != img_t1w.shape:
                    raise ValueError('The t1w and t2w cannot be paired since different size!')
                filename = get_name(t1w_nii_path)
                img_fdata_t1w = img_t1w.get_fdata()
                img_fdata_t2w = img_t2w.get_fdata()

                for i in tqdm(range(img_t1w.shape[direction])):
                    slice_t1w = get_slice(img_fdata_t1w, direction, i)
                    slice_t2w = get_slice(img_fdata_t2w, direction, i)
                    if float(np.count_nonzero(slice_t1w) / slice_t1w.size) >= preserving_ratio:
                        plt.imsave(
                            os.path.join(dataset_root + 't1w/',
                                         '{}.png'.format(filename + str(i) + 'd' + str(direction))),
                            slice_t1w, cmap='gray')
                        plt.imsave(
                            os.path.join(dataset_root + 't2w/',
                                         '{}.png'.format(filename + str(i) + 'd' + str(direction))),
                            slice_t2w, cmap='gray')
                        count += 1

        print("Save {} images in total".format(count))
