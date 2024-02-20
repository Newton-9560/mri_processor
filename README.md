# MRI to Paired Images/Numpy Dataset Converter and Viewer

This repository contains code for converting MRI (Magnetic Resonance Imaging) files into paired images (2D) or paired Numpy datasets (3D patch) and for viewing these paired images or datasets. Paired T1-weighted (T1w) and T2-weighted (T2w) MRI images are commonly used in medical imaging for various diagnostic and research purposes.

## Features

- **Conversion**: Convert MRI files into paired images (2D) or paired Numpy datasets (3D patch).
- **Visualization**: View paired T1w and T2w MRI images or Numpy datasets for qualitative analysis.
- **Interactive Viewer**: Use an interactive viewer to explore paired images or datasets and adjust visualization parameters.


## TODO: Generate 3-Dimensional Dataset

## Format
- [x] **Save**

Save the image in 3-D numpy file (or other format), depends on the efficiency of I/O

## Get Slice
- [x] set path size (args)
- [x] use nibabel get the array
- [x] define the bound according to the array size
- [x] implement a slide window

## View
- [x] show the 3-D data (specific method to be done)