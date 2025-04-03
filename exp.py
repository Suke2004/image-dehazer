import cv2
import numpy as np
from .model.image_dehazer import ImageDehazer
# Load your hazy image
hazy_image_path = '1.jpg'
hazy_image = cv2.imread(hazy_image_path)

# Remove haze using the provided code
dehazer = ImageDehazer()
dehazed_image, transmission_map = dehazer.remove_haze(hazy_image)

# Convert images to grayscale for simplicity
hazy_image_gray = cv2.cvtColor(hazy_image, cv2.COLOR_BGR2GRAY)
dehazed_image_gray = cv2.cvtColor(dehazed_image, cv2.COLOR_BGR2GRAY)

# Calculate noise image
noise_image = hazy_image_gray.astype(float) - dehazed_image_gray.astype(float)

# Compute variances
signal_variance = np.var(dehazed_image_gray)
noise_variance = np.var(noise_image)

# Calculate INR
inr = signal_variance / noise_variance
inr_db = 10 * np.log10(inr)

print(f"INR: {inr}")
print(f"INR (dB): {inr_db}")
