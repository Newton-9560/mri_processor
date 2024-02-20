from convert import DatasetGenerator, get_t2w_path, Dataset3DGenerator


def convert_name(name):
    return name.replace('space-T2w_', '')


if __name__ == '__main__':
    dataset_generator = Dataset3DGenerator('./data/mri', get_t2w_path)
    train, test = dataset_generator.get_t1w_path()

    dataset_generator.generate_dataset(train, './dataset/dataset3D/train/',
                                       preserving_ratio=0.8,
                                       patch_size=(32, 32, 32),
                                       stride=(32, 32, 32))
    dataset_generator.generate_dataset(test, './dataset/dataset3D/test/',
                                       preserving_ratio=0.8,
                                       patch_size=(32, 32, 32),
                                       stride=(32, 32, 32))
    # dataset_generator.generate_dataset(test, './dataset/test/')
