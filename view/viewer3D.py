import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def display_3d_image(image1, image2):
    fig, axs = plt.subplots(2, 3, figsize=(12, 8))
    plt.subplots_adjust(bottom=0.25, wspace=0.5)
    slice_indices = [0, 0, 0]

    slice_images1 = [image1[slice_indices[0], :, :],
                    image1[:, slice_indices[1], :],
                    image1[:, :, slice_indices[2]]]

    slice_images2 = [image2[slice_indices[0], :, :],
                     image2[:, slice_indices[1], :],
                     image2[:, :, slice_indices[2]]]

    imgs1 = [ax.imshow(slice_image, cmap='gray') for ax, slice_image in zip(axs[0], slice_images1)]
    imgs2 = [ax.imshow(slice_image, cmap='gray') for ax, slice_image in zip(axs[1], slice_images2)]

    slider_positions = [[0.1, 0.05], [0.4, 0.05], [0.7, 0.05]]  # Positions for sliders
    sliders = []
    for i, ax in enumerate(axs[0]):
        ax_slider = plt.axes([slider_positions[i][0], slider_positions[i][1], 0.2, 0.03],
                             facecolor='lightgoldenrodyellow')
        slider = Slider(ax_slider, 'Slice', 0, image1.shape[i] - 1, valinit=slice_indices[i], valstep=1)
        sliders.append(slider)

        def update(val, i=i):
            slice_indices[i] = int(sliders[i].val)
            slice_images1[i] = image1[slice_indices[0], :, :] if i == 0 else \
                image1[:, slice_indices[1], :] if i == 1 else \
                    image1[:, :, slice_indices[2]]
            imgs1[i].set_array(slice_images1[i])
            slice_images2[i] = image2[slice_indices[0], :, :] if i == 0 else \
                image2[:, slice_indices[1], :] if i == 1 else \
                    image2[:, :, slice_indices[2]]
            imgs2[i].set_array(slice_images2[i])
            fig.canvas.draw_idle()

        slider.on_changed(update)

    plt.show()


# Example usage:
# Generate a random 3D grayscale image (64x64x64)
image = np.load('../dataset/dataset3D/sub-CC00104XX05_ses-35800_desc-restore_41.npy')

# Display the image with scroll bars for each axis
display_3d_image(image[0], image[1])
