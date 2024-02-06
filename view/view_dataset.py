import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


# Function to load and display images from two folders
def display_images_with_filenames(folder1, folder2):
    # Get the list of files in each folder
    files1 = sorted([f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))])
    files2 = sorted([f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))])

    # Initialize current image index
    current_image_index = 0

    # Function to update the displayed image
    def update_image(event):
        nonlocal current_image_index
        current_image_index = (current_image_index + 1) % len(files1)
        img1.set_data(plt.imread(os.path.join(folder1, files1[current_image_index])))
        img2.set_data(plt.imread(os.path.join(folder2, files2[current_image_index])))
        title1.set_text(files1[current_image_index])
        title2.set_text(files2[current_image_index])
        plt.draw()

    # Create the figure and axes
    fig, ax = plt.subplots(1, 2)
    img1 = ax[0].imshow(plt.imread(os.path.join(folder1, files1[0])), 'gray')
    img2 = ax[1].imshow(plt.imread(os.path.join(folder2, files2[0])), 'gray')

    # Set titles with filenames
    title1 = ax[0].set_title(files1[0])
    title2 = ax[1].set_title(files2[0])

    # Remove axis ticks
    ax[0].axis('off')
    ax[1].axis('off')

    # Add a button to switch images
    ax_button = plt.axes([0.45, 0.05, 0.1, 0.075])
    button = Button(ax_button, 'Next')
    button.on_clicked(update_image)

    # Set space key to switch images
    def on_key(event):
        if event.key == ' ':
            update_image(event)

    fig.canvas.mpl_connect('key_press_event', on_key)

    plt.show()


# Example usage
# display_images('t1w', 't2w')  # Uncomment this line to run the function with your folders

# Note: This code assumes that the folders 't1w' and 't2w' are in the same directory as this script.
# Also, it assumes that the images are compatible with plt.imread (like .png or .jpg).

if __name__ == '__main__':
    display_images_with_filenames('./t1w2t2w/t1w/', './t1w2t2w/t2w/')
