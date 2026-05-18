import nd2
import numpy as np
from skimage.measure import shannon_entropy
from skimage.filters import sobel

#file_path = "/Users/tanmay/LenevoINFN/Work/BratatiImageJ/InFile/nd005.nd2"

def compute_mean_intensity(data, n_frames):
   
    mean_intensity = [] 
    for i in range(n_frames):

        frame = data[i].compute()

        mean_intensity.append(frame.mean())

    return np.array(mean_intensity)

def compute_statistics(data, n_frames):

    total_intensity = []
    maximum_intensity = []
    median_intensity = []

    for i in range(n_frames):

        frame = data[i].compute()

        total_intensity.append(frame.sum())
        maximum_intensity.append(frame.max())
        median_intensity.append(np.median(frame))

    return (
        np.array(total_intensity),
        np.array(maximum_intensity),
        np.array(median_intensity)
    )

def compute_structural_features(data, n_frames):

    variance_list = []
    entropy_list = []
    edge_strength_list = []
    fft_energy_list = []

    for i in range(n_frames):

        # -------------------------
        # Load frame lazily
        # -------------------------
        frame = data[i].compute()

        frame = frame.astype(np.float32)

        # -------------------------
        # VARIANCE
        # -------------------------
        variance = frame.var()

        # -------------------------
        # ENTROPY
        # -------------------------
        entropy = shannon_entropy(frame)

        # -------------------------
        # EDGE STRENGTH
        # -------------------------
        edges = sobel(frame)

        edge_strength = edges.mean()

        # -------------------------
        # FFT ENERGY
        # -------------------------
        fft = np.fft.fft2(frame)

        fft_shift = np.fft.fftshift(fft)

        fft_power = np.abs(fft_shift) ** 2

        fft_energy = fft_power.mean()

        # -------------------------
        # STORE
        # -------------------------
        variance_list.append(variance)

        entropy_list.append(entropy)

        edge_strength_list.append(edge_strength)

        fft_energy_list.append(fft_energy)

        print(f"[INFO] Processed frame {i+1}/{n_frames}")

    return (
        np.array(variance_list),
        np.array(entropy_list),
        np.array(edge_strength_list),
        np.array(fft_energy_list),
    )


def auto_roi_brightest_region(data, n_frames):

    print(f"[DEBUG] Data shape: {data.shape}")    # (94, 4656, 4656)
    first_frame = data[0].compute().astype(np.float32)

    # Find brightest pixel
    y, x = np.unravel_index(np.argmax(first_frame), first_frame.shape)

    # Define ROI size (adjustable)
    roi_size = 300

    y1 = max(0, y - roi_size//2)
    y2 = min(first_frame.shape[0], y + roi_size//2)

    x1 = max(0, x - roi_size//2)
    x2 = min(first_frame.shape[1], x + roi_size//2)

    auto_roi = (y1, y2, x1, x2)

    print(f"[DEBUG] Auto ROI: {auto_roi}")

    mean_intensity_roi = []

    for i in range (n_frames):
        frame = data[i].compute() 
        roi = frame[y1:y2, x1:x2]
        mean_intensity_roi.append(roi.mean())

    mean_intensity_roi = np.array(mean_intensity_roi)

    return mean_intensity_roi

import numpy as np
from scipy.ndimage import gaussian_filter


def auto_roi_gaussian_brightest_region(
    data,
    n_frames,
    roi_size=300,
    sigma=5,
):

    # -------------------------
    # First frame
    # -------------------------
    first_frame = data[0].compute().astype(np.float32)

    # -------------------------
    # Smooth image
    # -------------------------
    smooth = gaussian_filter(first_frame, sigma=sigma)

    # -------------------------
    # Find brightest region
    # -------------------------
    y, x = np.unravel_index(
        np.argmax(smooth),
        smooth.shape
    )

    # -------------------------
    # ROI boundaries
    # -------------------------
    y1 = max(0, y - roi_size // 2)

    y2 = min(first_frame.shape[0], y + roi_size // 2)

    x1 = max(0, x - roi_size // 2)

    x2 = min(first_frame.shape[1], x + roi_size // 2)

    print(f"[INFO] ROI center : ({y}, {x})")

    print(f"[INFO] ROI bounds : {(y1,y2,x1,x2)}")

    # -------------------------
    # Track ROI intensity
    # -------------------------
    roi_mean = []

    for i in range(n_frames):

        frame = data[i].compute()

        roi = frame[y1:y2, x1:x2]

        roi_mean.append(roi.mean())

    return np.array(roi_mean), (y1, y2, x1, x2)

def compute_intensity_timeframe(data,times, n_plots):

    # -----------------------------
    # INPUT
    # -----------------------------
    T = len(times)

    print(f"[DEBUG] Total frames: {T}")

    indices = np.linspace(
        0, 
        T - 1, 
        n_plots, 
        dtype=int
    )

    # -----------------------------
    # COMPUTE GLOBAL INTENSITY RANGE
    # -----------------------------
    sample_frames = []

    for i in indices:

        frame = data[i].compute().astype(np.float32)

        frame = np.nan_to_num(frame)

        sample_frames.append(frame)

    stack = np.stack(sample_frames)

    vmin = np.nanpercentile(stack, 1)

    vmax = np.nanpercentile(stack, 99)

    print(f"[DEBUG] vmin : {vmin}")

    print(f"[DEBUG] vmax : {vmax}")

    return vmin, vmax, data, indices    

