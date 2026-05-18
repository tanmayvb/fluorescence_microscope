import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import argparse
from pathlib import Path
from contextlib import contextmanager
import nd2
from fluorescence_loader.compute import compute_mean_intensity, compute_statistics, \
     compute_structural_features, auto_roi_brightest_region, \
     auto_roi_gaussian_brightest_region, compute_intensity_timeframe

parser = argparse.ArgumentParser()
parser.add_argument(
        "--file_path",
        type=Path,
        help="Folder with path containing nd2 files",
    )

parser.add_argument(
        "--plot_folder",
        type=Path,
        default="Output",
        help="Directory to write output plos directory",
    )

parser.add_argument(
    "--n_plots",
    type=int,
    default=10,
    help="Number of plots"
)
from contextlib import contextmanager
import nd2
import numpy as np


@contextmanager
def load_nd2_data(file_path):

    with nd2.ND2File(file_path) as f:

        data = f.to_dask()

        # -------------------------
        # timestamps
        # -------------------------
        if hasattr(f, "timestamps") and f.timestamps is not None:

            times = np.array(f.timestamps)

        else:

            events = f.events()

            times = np.array([
                e.get("time", np.nan)
                for e in events
            ])

        # -------------------------
        # safe frame count
        # -------------------------
        n_frames = min(
            len(times),
            data.shape[0]
        )

        times = times[:n_frames]

        yield data, times, n_frames

"""
def load_nd2_data(file_path, use_dask=True):

    #Load ND2 microscopy file safely and consistently.

    #Returns
    #-------
    #data : dask array or numpy array
    #    Image stack

    #times : np.ndarray
    #    Time stamps aligned with frames

    #n_frames : int
    #    Safe synchronized frame count
   

    f = nd2.ND2File(file_path)

    # -------------------------
    # Load image data
    # -------------------------
    if use_dask:
        data = f.to_dask()
    else:
        data = f.asarray()

    # -------------------------
    # Extract frame count
    # -------------------------
    metadata_frames = f.sizes.get('T', data.shape[0])

    data_frames = data.shape[0]

    # -------------------------
    # Extract timestamps
    # -------------------------
    if hasattr(f, "timestamps") and f.timestamps is not None:

        times = np.array(f.timestamps)

    else:

        events = f.events()

        times = np.array([
            e.get("time", np.nan)
            for e in events
        ])
    # -------------------------
    # Convert ms → sec if needed
    # -------------------------
    #if len(times) > 0 and np.nanmax(times) > 1000:
    #    times = times / 1000
    # -------------------------
    # Synchronize safely
    # -------------------------
    n_frames = min(
        len(times),
        metadata_frames,
        data_frames
    )

    times = times[:n_frames]

    print(f"[INFO] Data shape     : {data.shape}")
    print(f"[INFO] Metadata frames: {metadata_frames}")
    print(f"[INFO] Time points    : {len(times)}")
    print(f"[INFO] Safe frames    : {n_frames}")

    return f, data, times, n_frames
    f.close()
"""

def plot_intensity(mean_intensity, times, plot_directory):
    plt.plot(times, mean_intensity, marker='o')
    plt.xlabel("Time frame")
    plt.ylabel("Mean intensity")
    plt.title("Fluorescence Intensity vs Time")
    plt.grid()
    plt.savefig(f"{plot_directory}/Fluorescence_Intensity_with_Time.png")
    plt.savefig(f"{plot_directory}/Fluorescence_Intensity_with_Time.pdf")
    #plt.show()
    plt.close()

def plot_tot_max_median(tot, max_int, median, times, plot_directory):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, constrained_layout=True)

    # Plot on first axis
    ax1.plot(times, tot, 'tab:orange')
    ax1.set_xlabel("Time frame")
    ax1.set_title('Total Intensity')

    # Plot on second axis
    ax2.plot(times, max_int, 'tab:green')
    ax2.set_xlabel("Time frame")
    ax2.set_title('Maximum Intensity')
    
    ax3.plot(times, median, 'tab:purple')
    ax3.set_xlabel("Time frame")
    ax3.set_title('Median')
    plt.savefig(f"{plot_directory}/Time_Frame.png")
    plt.savefig(f"{plot_directory}/Time_Frame.pdf")
    #plt.show()
    plt.close()

import matplotlib.pyplot as plt


def plot_structural_features(
    times,
    variance,
    entropy,
    edge_strength,
    fft_energy,
    plot_directory,
):

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 8),
        constrained_layout=True
    )

    # -------------------------
    # Variance
    # -------------------------
    axes[0, 0].plot(times, variance)

    axes[0, 0].set_title("Variance")

    axes[0, 0].set_xlabel("Time")

    axes[0, 0].set_ylabel("Variance")

    # -------------------------
    # Entropy
    # -------------------------
    axes[0, 1].plot(times, entropy)

    axes[0, 1].set_title("Entropy")

    axes[0, 1].set_xlabel("Time")

    axes[0, 1].set_ylabel("Entropy")

    # -------------------------
    # Edge Strength
    # -------------------------
    axes[1, 0].plot(times, edge_strength)

    axes[1, 0].set_title("Edge Strength")

    axes[1, 0].set_xlabel("Time")

    axes[1, 0].set_ylabel("Edge Mean")

    # -------------------------
    # FFT Energy
    # -------------------------
    axes[1, 1].plot(times, fft_energy)

    axes[1, 1].set_title("FFT Energy")

    axes[1, 1].set_xlabel("Time")

    axes[1, 1].set_ylabel("FFT Energy")

    # -------------------------
    # Save
    # -------------------------
    plt.savefig(
        f"{plot_directory}/structural_features.png",
        dpi=300
    )

    plt.savefig(
        f"{plot_directory}/structural_features.pdf"
    )

    plt.close()

    print("[INFO] Structural feature plots saved")



def plot_auto_roi(times, mean_intensity, plot_directory=None, visroi=None, etx_txt=None):
    plt.plot(times, mean_intensity, marker='.', color= "green", linestyle='None')
    plt.xlabel("Time")
    if etx_txt:
        plt.ylabel("ROI Gauss intensity")
        plt.title("Auto ROI Gauss Intensity vs Time")
        plt.savefig(f"{plot_directory}/Auto_ROI_Gaussian_Intensity_Time.png")
        plt.savefig(f"{plot_directory}/Auto_ROI_Gaussian_Intensity_Time.pdf")
    else:
        plt.ylabel("ROI intensity")
        plt.title("Auto ROI Intensity vs Time")
        plt.savefig(f"{plot_directory}/Auto_ROI_Intensity_Time.png")
        plt.savefig(f"{plot_directory}/Auto_ROI_Intensity_Time.pdf")
    plt.close()
    #plt.show()

    if(visroi):
        plt.imshow(first_frame, cmap='gray')
        plt.scatter([x], [y], color='red', s=50)
        plt.title("Auto ROI center")
        plt.savefig("{plot_directory}/Auto_ROI_center.png")
        plt.savefig("{plot_directory}/Auto_ROI_center.pdf")
        plt.close()
        #plt.show()

def plot_xy_intensity(vmin, vmax, data, indices, n_plots = 10, plot_directory=None):
    # -----------------------------
    # CREATE GRID PLOT
    # -----------------------------
    ncols = 5
    nrows = int(np.ceil(n_plots / ncols))

    # -----------------------------
    # SELECT FRAMES (evenly spaced)
    # -----------------------------

    #indices = np.linspace(0, T - 1, n_plots, dtype=int)
    print(f"Selected frames: {indices}")


    fig, axes = plt.subplots(2, 5, figsize=(15, 6))

    axes = axes.ravel()

    # -----------------------------
    # PLOT EACH FRAME (X,Y IMAGE)
    # -----------------------------
    for ax, idx in zip(axes, indices):
        frame = data[idx].compute()

        frame = np.nan_to_num(
            frame.astype(np.float32),
            nan=0.0,
            posinf=0.0,
            neginf=0.0
        )

        im = ax.imshow(frame, cmap='afmhot', vmin=vmin, vmax=vmax)
        ax.set_title(f"T={idx}")
        ax.axis('off')

    plt.subplots_adjust(wspace=0.1, hspace=0.3)
    #plt.show()

    plt.savefig(f"{plot_directory}/time_series_grid.png")
    plt.savefig(f"{plot_directory}/time_series_grid.pdf")
    plt.close()


def main():
    print(f"\n===============\033[92m Starting Main: Compute and Plotting \033[0m=======================\n")

    args = parser.parse_args()
    infile = args.file_path

    if not infile:
        raise ValueError("Please provide a valid nd2 file !!") 
    else:
        print(f"Input Files Processing : {infile}")

    #file, data, times, n_frames = load_nd2_data(infile)

    # Make Plots directory 
    plot_directory = args.plot_folder
    Path(plot_directory).mkdir(parents=True, exist_ok=True)
    print("Directory : ", plot_directory)

    ###########################################
    # Load file 
    ###########################################
    with load_nd2_data(infile) as (
        data,
        times,
        n_frames
    ):

        # -------------------------
        # Compute descriptors
        # -------------------------
        print(f"Staring computions")
        mean_intensity = compute_mean_intensity(
            data,
            n_frames
        )

        tot_intensity, max_intensity, med_intensity = compute_statistics(
            data,
            n_frames
        )
    
        variance, entropy, edge_strength, fft_energy = compute_structural_features(
            data,
            n_frames
        )

        intensity_roi_mean = auto_roi_brightest_region(
            data,
            n_frames
        )

        intensity_roi_mean_gaussian, roi = auto_roi_gaussian_brightest_region(
            data,
            n_frames
        )
 
        if args.n_plots:
           num = args.n_plots
        else:
             num = n_frame

        vmin, vmax, data_intensity, indices  = compute_intensity_timeframe(
            data,
            times,
            num
        )
        print(f"computions runs sucessfully")

    # -------------------------
    # plotting is safe
    # -------------------------
    print(times.shape)
    print(mean_intensity.shape)
    plot_intensity(
        times, 
        mean_intensity, 
        plot_directory\
    )

    plot_intensity(
        times,
        mean_intensity,
        plot_directory\
    )

    plot_tot_max_median(
        times,
        tot_intensity,
        max_intensity,
        med_intensity,
        plot_directory
    )

    plot_structural_features(
        times,
        variance,
        entropy,
        edge_strength,
        fft_energy,
        plot_directory
    )

    plot_auto_roi(
        times,
        intensity_roi_mean,
        plot_directory
    )

    plot_auto_roi(
        times,
        intensity_roi_mean_gaussian,
        plot_directory,
        etx_txt=True
    )

    if args.n_plots:
        n_plots = args.n_plots
    else:
        n_plots = len(times) 
    plot_xy_intensity(
        vmin, 
        vmax, 
        data_intensity, 
        indices, 
        n_plots, 
        plot_directory
    )
    #time = np.arange(len(intensity_roi_mean))

    print("\n==================\033[92mRun Sucessfully\033[0m========================")
    print(f"All plots saved in the folder:  {plot_directory} \n")


if __name__ == "__main__":
    main()


