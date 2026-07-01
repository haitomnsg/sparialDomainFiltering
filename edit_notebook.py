import json

def main():
    with open('Spatial_Domain_Filtering_Lab.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # We will find the cells and add visualizations where appropriate.
    
    # 1. Visualization for Experiment 1
    # Find the cell with "for s, r in zip(sigmas, results_gauss):"
    exp1_eval_idx = -1
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code' and 'results_gauss' in ''.join(cell['source']) and 'psnr' in ''.join(cell['source']):
            exp1_eval_idx = i
            break
            
    if exp1_eval_idx != -1:
        plot_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, axes = plt.subplots(2, 4, figsize=(16, 8))\n",
                "axes[0, 0].imshow(noisy, cmap='gray', vmin=0, vmax=1)\n",
                "axes[0, 0].set_title('Noisy Image')\n",
                "axes[0, 0].axis('off')\n",
                "for i, (k, r) in enumerate(zip(sizes, results_box)):\n",
                "    axes[0, i+1].imshow(r, cmap='gray', vmin=0, vmax=1)\n",
                "    axes[0, i+1].set_title(f'Box Filter k={k}')\n",
                "    axes[0, i+1].axis('off')\n",
                "axes[1, 0].imshow(noisy, cmap='gray', vmin=0, vmax=1)\n",
                "axes[1, 0].set_title('Noisy Image')\n",
                "axes[1, 0].axis('off')\n",
                "for i, (s, r) in enumerate(zip(sigmas, results_gauss)):\n",
                "    axes[1, i+1].imshow(r, cmap='gray', vmin=0, vmax=1)\n",
                "    axes[1, i+1].set_title(f'Gaussian Filter s={s}')\n",
                "    axes[1, i+1].axis('off')\n",
                "plt.tight_layout()\n",
                "plt.show()\n"
            ]
        }
        # Check if already added
        if ''.join(nb['cells'][exp1_eval_idx+1]['source']).startswith("fig, axes = plt.subplots(2, 4"):
            pass
        else:
            nb['cells'].insert(exp1_eval_idx + 1, plot_cell)
            
    # 2. Visualization for Experiment 2
    # Find the cell with "sharp_after_smooth = np.clip"
    exp2_idx = -1
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code' and 'sharp_after_smooth' in ''.join(cell['source']):
            exp2_idx = i
            break
            
    if exp2_idx != -1:
        plot_cell2 = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, axes = plt.subplots(2, 3, figsize=(15, 10))\n",
                "axes[0, 0].imshow(img, cmap='gray', vmin=0, vmax=1)\n",
                "axes[0, 0].set_title('Original')\n",
                "axes[0, 0].axis('off')\n",
                "axes[0, 1].imshow(sharp_4, cmap='gray', vmin=0, vmax=1)\n",
                "axes[0, 1].set_title('Sharpened (Laplacian 4)')\n",
                "axes[0, 1].axis('off')\n",
                "axes[0, 2].imshow(sharp_8, cmap='gray', vmin=0, vmax=1)\n",
                "axes[0, 2].set_title('Sharpened (Laplacian 8)')\n",
                "axes[0, 2].axis('off')\n",
                "axes[1, 0].imshow(noisy, cmap='gray', vmin=0, vmax=1)\n",
                "axes[1, 0].set_title('Noisy')\n",
                "axes[1, 0].axis('off')\n",
                "axes[1, 1].imshow(sharp_noisy_4, cmap='gray', vmin=0, vmax=1)\n",
                "axes[1, 1].set_title('Sharpened Noisy (Laplacian 4)')\n",
                "axes[1, 1].axis('off')\n",
                "axes[1, 2].imshow(sharp_after_smooth, cmap='gray', vmin=0, vmax=1)\n",
                "axes[1, 2].set_title('Smoothed then Sharpened')\n",
                "axes[1, 2].axis('off')\n",
                "plt.tight_layout()\n",
                "plt.show()\n"
            ]
        }
        if ''.join(nb['cells'][exp2_idx+1]['source']).startswith("fig, axes = plt.subplots(2, 3"):
            pass
        else:
            nb['cells'].insert(exp2_idx + 1, plot_cell2)

    # 3. Visualization for Experiment 3
    # Find the cell with "for sigma in [0.5, 1.0, 2.0, 4.0]:"
    exp3_idx = -1
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code' and 'for sigma in [0.5, 1.0, 2.0, 4.0]:' in ''.join(cell['source']):
            exp3_idx = i
            break
            
    if exp3_idx != -1:
        # We need to change the loop to actually store and display results
        nb['cells'][exp3_idx]['source'] = [
            "fig, axes = plt.subplots(2, 4, figsize=(16, 8))\n",
            "sigmas_um = [0.5, 1.0, 2.0, 4.0]\n",
            "for i, sigma in enumerate(sigmas_um):\n",
            "    result, mask = unsharp_mask(img, sigma=sigma, k=1.0)\n",
            "    axes[0, i].imshow(mask, cmap='RdBu_r', vmin=-0.2, vmax=0.2)\n",
            "    axes[0, i].set_title(f'Mask (sigma={sigma})')\n",
            "    axes[0, i].axis('off')\n",
            "    axes[1, i].imshow(result, cmap='gray', vmin=0, vmax=1)\n",
            "    axes[1, i].set_title(f'Sharpened (sigma={sigma})')\n",
            "    axes[1, i].axis('off')\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ]

    with open('Spatial_Domain_Filtering_Lab_modified.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

if __name__ == '__main__':
    main()
