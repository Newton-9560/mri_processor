import numpy as np


def get_name(s):
    last_slash_index = s.rfind('/')
    nii_index = s.find('.nii', last_slash_index)

    if last_slash_index != -1 and nii_index != -1:
        return s[last_slash_index + 1:nii_index - 3]
    else:
        raise ValueError("This is not a nii file!")


def get_slice(img, direction, index):
    if direction == 2:
        return img[:, :, index].astype(np.uint8)
    elif direction == 1:
        return img[:, index, :].astype(np.uint8)
    elif direction == 0:
        return img[index, :, :].astype(np.uint8)
    else:
        raise ValueError("Invalid direction. Must be 0, 1, or 2.")
