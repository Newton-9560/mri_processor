from convert import DatasetGenerator, get_t2w_path


def convert_name(name):
    return name.replace('space-T2w_', '')


if __name__ == '__main__':
    dataset_generator = DatasetGenerator('./data/mri', get_t2w_path)
    # dataset_generator.file_preprocess(convert_name)
    # dataset_generator.get_t1w_path()
    # dataset_generator.t1w_path = ['./data/mri/sub-CC00149XX18_ses-49000_desc-restore_T1w.nii.gz']

    dataset_generator.generate_dataset('./dataset/train/')
