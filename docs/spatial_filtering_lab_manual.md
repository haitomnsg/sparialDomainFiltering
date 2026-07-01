## **KATHMANDU UNIVERSITY** 

School of Engineering 

## **DEPARTMENT OF ARTIFICIAL INTELLIGENCE** 

B.Tech. in Artificial Intelligence 

## **AICL 311 Image Processing** 

**Laboratory** 

_Lab Manual and Notebook_ 

## **Module: Spatial Domain Filtering** 

_Topics: Smoothing Filters, Sharpening Filters, Unsharp Masking, High-Boost Filtering_ 

Date: June 22, 2026 

1 

## **1.  Background Theory** 

## **1.1  The Spatial Domain** 

In image processing, the spatial domain refers to the image plane itself. Operations in the spatial domain act directly on the pixel values of an image, as opposed to frequency-domain methods that first transform the image (e.g. using the Fourier transform) and then manipulate the transformed coefficients. 

Let f(x, y) denote a digital image of size M × N, where x ∈ {0, 1, ..., M−1} and y ∈ {0, 1, ..., N−1}. The fundamental operation in spatial domain processing is the convolution (or, for symmetric kernels, correlation) of the image with a filter kernel w of size m × n: 

g(x, y) = Σs Σt w(s, t) · f(x+s, y+t) 

where s and t range over the kernel dimensions. In NumPy and OpenCV, this is implemented via scipy.ndimage.convolve or cv2.filter2D. **The choice of kernel w determines whether the filter smooths, sharpens, or enhances edges.** 

## **1.2  Smoothing Filters** 

Smoothing filters reduce noise and fine detail by replacing each pixel with a weighted combination of its neighbours. Two classical variants are the box (mean) filter and the Gaussian filter. 

## **1.2.1  Box (Mean) Filter** 

The box filter averages all pixels in a neighbourhood of size m × n uniformly: 

w_box(s,t) = 1/(mn)  for all (s,t) in the kernel 

It is computationally cheap but introduces a characteristic blurring artifact: straight edges become ramp-like transitions and ringing can appear. For a 3×3 kernel: 

||||
|---|---|---|
|1/9|1/9|1/9|
|1/9|1/9|1/9|
|1/9|1/9|1/9|



## **1.2.2  Gaussian Filter** 

The Gaussian filter uses weights derived from the 2D Gaussian function: 

w_G(s,t) = (1 / 2πσ²) · exp( −(s² + t²) / 2σ² ) 

The parameter σ (standard deviation) controls the spread of the smoothing. A larger σ produces heavier blurring. The Gaussian kernel has the important property that it is separable: a 2D convolution with the kernel can be decomposed into two 1D convolutions (first along rows, then along columns), which reduces computation from O(m²) to O(2m) multiplications per pixel. 

Practically speaking, Gaussian smoothing is preferred over the box filter because it does not introduce frequency-domain ringing. The Gaussian is the only function that is simultaneously optimal in the spatial and frequency domains, making it the default choice for anti-aliasing and preprocessing before edge detection. 

2 

## **1.3  Sharpening Filters** 

Sharpening enhances edges and fine structure by emphasizing local intensity differences. The mathematical basis is the Laplacian operator, which measures the second spatial derivative of the image. 

## **1.3.1  The Laplacian** 

For a continuous function f(x,y), the Laplacian is: 

## ∇² f = ∂²f/∂x² + ∂²f/∂y² 

In discrete images, the second partial derivatives are approximated by finite differences. The most common 3×3 Laplacian kernels are: 

## **Laplacian kernel (without diagonals):** 

||||
|---|---|---|
|0|−1|0|
|−1|4|−1|
|0|−1|0|



## **Laplacian kernel (with diagonals):** 

−1 −1 −1 −1 8 −1 −1 −1 −1 

To sharpen, the Laplacian response is subtracted from the original image (because the Laplacian measures intensity changes; subtracting it from the original amplifies peaks and troughs): 

g(x,y) = f(x,y) − ∇² f(x,y) 

Equivalently, this can be achieved with a single combined kernel: 

0 −1 0 −1 5 −1 0 −1 0 

## **1.4  Unsharp Masking** 

Unsharp masking is a classical photographic technique adapted for digital use. The name is counterintuitive: it sharpens by subtracting a blurred (unsharp) version of the image. 

Let f_smooth be a smoothed version of the original image f. The mask (the detail signal) is: 

f_mask(x,y) = f(x,y) − f_smooth(x,y) 

3 

The sharpened image is then: 

g(x,y) = f(x,y) + k · f_mask(x,y) 

where k ≥ 1 is a scaling factor. When k = 1, this is standard unsharp masking. The effect is to add edge information back into the image. Edges appear as regions where f and f_smooth differ significantly; in flat regions, f_mask ≈ 0 and the original image is preserved. 

Substituting the mask definition: 

g(x,y) = f(x,y) + k · [f(x,y) − f_smooth(x,y)] 

- = (1+k) · f(x,y) − k · f_smooth(x,y) 

This form makes clear that unsharp masking is a linear combination of the original and its blurred version, with a specific relationship between coefficients. 

## **1.5  High-Boost Filtering** 

High-boost filtering generalizes unsharp masking by allowing k > 1, which amplifies the detail signal beyond simple restoration: 

g(x,y) = A · f(x,y) − f_smooth(x,y) 

where A ≥ 1. When A = 1, we recover standard unsharp masking (with k=1). When A > 1, the highfrequency components of the image are amplified relative to the low-frequency base. 

Expanding the expression with A = 1 + k: 

g = (1+k) · f − k · f_smooth 

As k increases, the filter progressively emphasises high-frequency content. 

4 

## **2.  Experiment 1: Spatial Smoothing Filters** 

## **2.1  Procedure** 

## **Step 1: Setting up the environment** 

import numpy as np import cv2 import matplotlib.pyplot as plt from scipy.ndimage import convolve, gaussian_filter 

# Load a grayscale image img = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE) img = img.astype(np.float64) / 255.0   # normalise to [0, 1] 

# Add Gaussian noise for testing np.random.seed(42) noise_sigma = 0.05 noisy = img + np.random.normal(0, noise_sigma, img.shape) noisy = np.clip(noisy, 0, 1) 

## **Step 2: Mean (Box) Filter** 

def box_filter(image, kernel_size): 

k = kernel_size 

kernel = np.ones((k, k), dtype=np.float64) / (k * k) 

return convolve(image, kernel, mode='reflect') 

sizes = [3, 7, 15] 

results_box = [box_filter(noisy, k) for k in sizes] 

## **Step 3: Gaussian Filter** 

def gaussian_filter_custom(image, sigma): 

return gaussian_filter(image, sigma=sigma, mode='reflect') 

sigmas = [0.5, 1.5, 3.0] 

results_gauss = [gaussian_filter_custom(noisy, s) for s in sigmas] 

## **Step 4: Quantitative Evaluation** 

Compute the Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM) for each filtered result against the clean original. Record these values in your notebook. 

from skimage.metrics import peak_signal_noise_ratio as psnr from skimage.metrics import structural_similarity as ssim 

5 

print('Method'.ljust(20), 'PSNR (dB)'.ljust(15), 'SSIM') print('-' * 45) for k, r in zip(sizes, results_box): p = psnr(img, r, data_range=1.0) s = ssim(img, r, data_range=1.0) print(f'Box k={k}'.ljust(20), f'{p:.2f}'.ljust(15), f'{s:.4f}') for sig, r in zip(sigmas, results_gauss): p = psnr(img, r, data_range=1.0) s = ssim(img, r, data_range=1.0) print(f'Gaussian s={sig}'.ljust(20), f'{p:.2f}'.ljust(15), f'{s:.4f}') 

## **2.5  Observations** 

Record the following in your lab notebook as you run the experiments. Do not copy the expected answers from here; note what you actually observe. 

- Describe visually how each filter changes the appearance of the image. 

- At what kernel size or sigma does the image begin to lose recognisable detail? 

- Compare PSNR values across box and Gaussian filters for similar smoothing strengths. Which is better? 

- Look at edges in the filtered images. Does the box filter preserve edges better or worse than the Gaussian? 

## **3.  Experiment 2: Sharpening Filters using the Laplacian** 

## **3.1  Procedure** 

## **Step 1: Apply the Laplacian** 

# Two standard Laplacian kernels lap_4 = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=np.float64) lap_8 = np.array([[-1, -1, -1], [-1,  8, -1], [-1, -1, -1]], dtype=np.float64) laplacian_4 = convolve(img, lap_4, mode='reflect') laplacian_8 = convolve(img, lap_8, mode='reflect') # Sharpen by subtracting Laplacian from original sharp_4 = img - laplacian_4 sharp_8 = img - laplacian_8 

6 

# Clip to valid range sharp_4 = np.clip(sharp_4, 0, 1) sharp_8 = np.clip(sharp_8, 0, 1) 

## **Step 2: Effect on a noisy image** 

# Apply sharpening to the noisy image sharp_noisy_4 = np.clip(noisy - convolve(noisy, lap_4, mode='reflect'), 0, 1) 

# Compare with: first smooth, then sharpen smoothed_first = gaussian_filter(noisy, sigma=1.0) sharp_after_smooth = np.clip(smoothed_first - convolve(smoothed_first, lap_4, mode='reflect'), 0, 1) 

## **4.  Experiment 3: Unsharp Masking** 

## **4.1  Procedure** 

## **Step 1: Basic unsharp masking** 

def unsharp_mask(image, sigma, k=1.0): """ 

image  : input image (float64, values in [0,1]) sigma  : standard deviation for Gaussian smoothing k      : strength of sharpening (k=1 is standard unsharp masking) """ 

blurred = gaussian_filter(image, sigma=sigma, mode='reflect') mask = image - blurred sharpened = image + k * mask return np.clip(sharpened, 0, 1), mask 

# Vary sigma with fixed k for sigma in [0.5, 1.0, 2.0, 4.0]: result, mask = unsharp_mask(img, sigma=sigma, k=1.0) # save result and mask for reporting 

## **Step 2: Vary the sharpening strength** 

sigma_fixed = 1.0 for k in [0.5, 1.0, 2.0, 5.0]: result, mask = unsharp_mask(img, sigma=sigma_fixed, k=k) # Compute PSNR relative to original 

p = psnr(img, result, data_range=1.0) 

7 

print(f'k={k}  PSNR={p:.2f} dB') 

## **Step 3: Visualise the mask** 

_, mask = unsharp_mask(img, sigma=1.0, k=1.0) 

# The mask has both positive and negative values # Display using a diverging colormap fig, axes = plt.subplots(1, 3, figsize=(12, 4)) axes[0].imshow(img, cmap='gray', vmin=0, vmax=1) axes[0].set_title('Original') axes[1].imshow(mask, cmap='RdBu_r', vmin=-0.2, vmax=0.2) axes[1].set_title('Unsharp Mask (detail signal)') axes[2].imshow(img + mask, cmap='gray', vmin=0, vmax=1) axes[2].set_title('Sharpened (k=1)') plt.tight_layout() plt.savefig('unsharp_mask_visualisation.png', dpi=150) 

## **5.  Experiment 4: High-Boost Filtering** 

## **5.1  Procedure** 

## **- Step 1: Implement high boost filtering** 

def high_boost_filter(image, sigma, A): """ image  : float64 image in [0,1] sigma  : Gaussian blur sigma for the low-pass step A      : boost factor (A >= 1) """ blurred = gaussian_filter(image, sigma=sigma, mode='reflect') high_boost = A * image - blurred return np.clip(high_boost, 0, 1) 

# Note: A * f - f_smooth = f + (A-1)*f - f_smooth #                        = f + (A-1)*f - f_smooth # With k = A - 1: = f + k*(f - f_smooth) # This confirms the relationship with unsharp masking 

## **Step 2: Vary A** 

sigma_hb = 1.5 boost_factors = [1.0, 1.5, 2.0, 3.0, 5.0] results_hb = [high_boost_filter(img, sigma_hb, A) for A in boost_factors] 

8 

fig, axes = plt.subplots(1, len(boost_factors), figsize=(18, 4)) for ax, A, r in zip(axes, boost_factors, results_hb): ax.imshow(r, cmap='gray', vmin=0, vmax=1) ax.set_title(f'A = {A}') ax.axis('off') plt.tight_layout() plt.savefig('high_boost_comparison.png', dpi=150) 

9 

