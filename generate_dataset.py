import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt
from tqdm import tqdm
from utils import get_name, get_slice, get_t2w_path

filenames_t1w = ['./anat/sub-CC00054XX05_ses-8800_T1w.nii.gz',
                 './anat/sub-CC00054XX05_ses-8800_desc-restore_T1w.nii.gz']
dataset_root = './t1w&t2w/'
directions = [0, 1, 2]
preserving_ratio = 0.2


def generate_dataset():
    if not os.path.exists(dataset_root):
        os.mkdir(dataset_root)
        os.mkdir(dataset_root + 't1w')
        os.mkdir(dataset_root + 't2w')
        print("Create new dataset in {}".format(dataset_root))
    else:
        print("Add data into existed folder {}".format(dataset_root))

    count = 0
    for direction in directions:
        for t1w_nii_path in filenames_t1w:
            img_t1w = nib.load(t1w_nii_path)
            img_t2w = nib.load(get_t2w_path(t1w_nii_path))
            if img_t2w.shape != img_t1w.shape:
                raise ValueError('The t1w and t2w cannot be paired since different size!')
            filename = get_name(t1w_nii_path)
            img_fdata_t1w = img_t1w.get_fdata()
            img_fdata_t2w = img_t2w.get_fdata()
            # print(img_fdata_t1w[100][120][120])

            for i in tqdm(range(img_t1w.shape[direction])):
                slice_t1w = get_slice(img_fdata_t1w, direction, i)
                slice_t2w = get_slice(img_fdata_t2w, direction, i)
                if float(np.count_nonzero(slice_t1w) / slice_t1w.size) >= preserving_ratio:
                    plt.imsave(
                        os.path.join(dataset_root + 't1w/', '{}.png'.format(filename + str(i) + 'd' + str(direction))),
                        slice_t1w, cmap='gray')
                    plt.imsave(
                        os.path.join(dataset_root + 't2w/', '{}.png'.format(filename + str(i) + 'd' + str(direction))),
                        slice_t2w, cmap='gray')
                    count += 1

    print("Save {} images in total".format(count))


if __name__ == '__main__':
    generate_dataset()
