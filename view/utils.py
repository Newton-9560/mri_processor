import nibabel as nib
from nibabel.viewers import OrthoSlicer3D


def show_mri(filename):
    img = nib.load(filename)
    print(img.header['db_name'])

    OrthoSlicer3D(img.dataobj).show()


if __name__ == '__main__':
    show_mri('../data/mri/sub-CC00152AN04_ses-49200_desc-restore_T1w.nii.gz')
