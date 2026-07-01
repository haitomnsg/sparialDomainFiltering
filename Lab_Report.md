# Lab Report: Spatial Domain Filtering

## 1. Objectives
- To understand the fundamental concepts of spatial domain filtering in image processing.
- To implement and analyze spatial smoothing filters, specifically the Box (Mean) filter and the Gaussian filter, and observe their effects on noise reduction and image blurring.
- To implement Laplacian sharpening to enhance the edges and fine details of an image.
- To understand and apply unsharp masking and high-boost filtering techniques for image sharpening and detail amplification.
- To evaluate the performance of different filters using quantitative metrics such as Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM).

## 2. Theory
### 2.1 The Spatial Domain
In image processing, spatial domain operations act directly on the pixel values of an image. The fundamental operation is convolution (or correlation) of the image with a filter kernel. The choice of kernel determines whether the filter smooths, sharpens, or enhances edges in the image.

### 2.2 Smoothing Filters
Smoothing filters are primarily used for noise reduction and blurring. They replace each pixel with a weighted combination of its neighbors.
- **Box (Mean) Filter**: Averages all pixels uniformly in a given neighborhood. While computationally inexpensive, it often introduces blurring artifacts such as ramp-like transitions on straight edges and ringing.
- **Gaussian Filter**: Uses weights derived from a 2D Gaussian function. The standard deviation parameter ($\sigma$) controls the degree of blurring. Gaussian smoothing is generally preferred as it does not introduce frequency-domain ringing and is optimal in both spatial and frequency domains.

### 2.3 Sharpening Filters
Sharpening filters enhance edges and fine details by emphasizing local intensity differences.
- **Laplacian Filter**: A sharpening filter based on the second spatial derivative of the image. It highlights rapid intensity transitions. The sharpened image is obtained by subtracting the Laplacian response from the original image, which amplifies peaks and troughs.

### 2.4 Unsharp Masking and High-Boost Filtering
- **Unsharp Masking**: A technique that sharpens an image by subtracting a blurred version of the image from the original. This difference, called the mask (or detail signal), is then scaled and added back to the original image to restore and enhance edge information.
- **High-Boost Filtering**: A generalization of unsharp masking where the original image is multiplied by an amplification factor ($A \ge 1$) before subtracting the blurred image. This results in the high-frequency components being amplified relative to the low-frequency base, giving a sharper image.

## 3. Conclusion
In this laboratory experiment, various spatial domain filtering techniques were successfully implemented and evaluated. Spatial smoothing filters (Box and Gaussian) effectively reduced noise, with the Gaussian filter demonstrating superior visual quality by avoiding ringing artifacts. Sharpening filters, including the Laplacian, effectively highlighted rapid intensity transitions, enhancing the edges of the image. Furthermore, unsharp masking and high-boost filtering proved to be versatile methods for controlling the degree of sharpening, restoring edge information, and amplifying high-frequency details. The results were consistent with theoretical expectations and demonstrated the utility of spatial filtering in image enhancement.
