import os
from tqdm import tqdm
import nibabel as nib
import numpy as np

from .generate_dataset import DatasetGenerator
from .utils import get_name


class Dataset3DGenerator(DatasetGenerator):
    def __init__(self, source_root, get_t2w_path_from_t1w):
        super().__init__(source_root, get_t2w_path_from_t1w)

    def generate_dataset(self, t1w_path, dataset_root, preserving_ratio=0.4,
                         directions=None, patch_size=(64, 64, 64), stride=(32, 32, 32)):
        if not os.path.exists(dataset_root):
            os.makedirs(dataset_root)
            os.mkdir(dataset_root + 't1w')
            os.mkdir(dataset_root + 't2w')
            print("Create new dataset in {}".format(dataset_root))
        else:
            print("Add data into existing folder {}".format(dataset_root))

        count = 0
        for t1w_nii_path in tqdm(t1w_path):
            img_t1w = nib.load(t1w_nii_path).get_fdata()
            img_t2w = nib.load(self.get_t2w_path(t1w_nii_path)).get_fdata()
            if img_t2w.shape != img_t1w.shape:
                raise ValueError('The t1w and t2w cannot be paired since different size!')
            filename = get_name(t1w_nii_path)

            serial_num = 0
            for i in range(0, img_t1w.shape[0] - patch_size[0], stride[0]):
                for j in range(0, img_t1w.shape[1] - patch_size[1], stride[1]):
                    for k in range(0, img_t1w.shape[2] - patch_size[2], stride[2]):
                        patch_t1w = img_t1w[i:i + patch_size[0], j:j + patch_size[1], k:k + patch_size[2]]
                        patch_t2w = img_t2w[i:i + patch_size[0], j:j + patch_size[1], k:k + patch_size[2]]
                        if ((np.count_nonzero(patch_t1w) / patch_t1w.size) +
                            (np.count_nonzero(patch_t2w) / patch_t2w.size)) / 2 >= preserving_ratio:
                            count += 1
                            np.save(os.path.join(dataset_root, '{}.npy'.format(filename + str(serial_num))),
                                    np.array([patch_t1w, patch_t2w]))
                            serial_num += 1

        print("Save {} images in total".format(count))
