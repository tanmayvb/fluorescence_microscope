import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import argparse
from fluorescence_loader.compute_intensity import Compute_with_asrry, ComputeMean_with_asrry, Compute_tot_max, Auto_ROI_brightest_region, Compute_intensity_timeframe


parser = argparse.ArgumentParser()
parser.add_argument(
        "--file_path",
        type=Path,
        help="Folder with path containing nd2 files",
    )

def plot_intensity(mean_intensity):
    plt.plot(mean_intensity, marker='o')
    plt.xlabel("Time frame")
    plt.ylabel("Mean intensity")
    plt.title("Fluorescence Intensity vs Time")
    plt.grid()
    plt.savefig('Fluorescence_Intensity_with_Time.png')
    plt.savefig('Fluorescence_Intensity_with_Time.pdf')
    #plt.show()
    plt.close()

def plot_intensity_realtime(times, mean_intensity):
    plt.plot(times, mean_intensity, marker='o')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Mean intensity")
    plt.title("Intensity vs Time (real time)")
    plt.grid()
    plt.savefig('Intensity_with_Real_Time.png')
    plt.savefig('Intensity_with_Real_Time.pdf')
    #plt.show()
    plt.close()

def plot_tot_max_median(tot, max_int, median):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, constrained_layout=True)

    # Plot on first axis
    ax1.plot(tot, 'tab:orange')
    ax1.set_xlabel("Time frame")
    ax1.set_title('Total Intensity')

    # Plot on second axis
    ax2.plot(max_int, 'tab:green')
    ax2.set_xlabel("Time frame")
    ax2.set_title('Maximum Intensity')
    
    ax3.plot(max_int, 'tab:purple')
    ax3.set_xlabel("Time frame")
    ax3.set_title('Median')
    plt.savefig('Time_Frame.png')
    plt.savefig('Time_Frame.pdf')
    #plt.show()
    plt.close()
 
    plt.show()

def plot_auto_roi(time, mean_intensity, visroi=None):
    plt.plot(time, mean_intensity, marker='.', color= "green", linestyle='None')
    plt.xlabel("Time")
    plt.ylabel("ROI intensity")
    plt.title("Auto ROI Intensity vs Time")
    plt.savefig('Auto_ROI_Intensity_Time.png')
    plt.savefig('Auto_ROI_Intensity_Time.pdf')
    plt.close()
    #plt.show()

    if(visroi):
        plt.imshow(first_frame, cmap='gray')
        plt.scatter([x], [y], color='red', s=50)
        plt.title("Auto ROI center")
        plt.savefig('Auto_ROI_center.png')
        plt.savefig('Auto_ROI_center.pdf')
        plt.close()
        #plt.show()

def plot_xy_intensity(vmin, vmax, data, indices, n_plots = 10):
    # -----------------------------
    # CREATE GRID PLOT
    # -----------------------------
    ncols = 5
    nrows = int(np.ceil(n_plots / ncols))

    # -----------------------------
    # SELECT FRAMES (evenly spaced)
    # -----------------------------

    #indices = np.linspace(0, T - 1, n_plots, dtype=int)
    print("Selected frames:", indices)


    fig, axes = plt.subplots(2, 5, figsize=(15, 6))

    axes = axes.ravel()

    # -----------------------------
    # PLOT EACH FRAME (X,Y IMAGE)
    # -----------------------------
    for ax, idx in zip(axes, indices):
        frame = data[idx].compute()

        im = ax.imshow(frame, cmap='gray', vmin=vmin, vmax=vmax)
        ax.set_title(f"T={idx}")
        ax.axis('off')

    plt.subplots_adjust(wspace=0.1, hspace=0.3)
    #plt.show()

    plt.savefig("time_series_grid.png")
    plt.savefig("time_series_grid.pdf")
    plt.close()


def main():

    args = parser.parse_args()
    infile = args.file_path
    if not infile:
        raise ValueError("Please input a valid nd2 file !!") 
    else:
        print(f"Input Files Processing : {infile}")

    mean_intensity = ComputeMean_with_asrry(infile)
    #print("Intensity", mean_intensity)

    #time = RealTime_Extract()
       
    mean_intensity = np.array(mean_intensity)

    # x-axis (time index)
    time = np.arange(len(mean_intensity))

    print("time shape:", np.shape(time))
    print("mean shape:", np.shape(mean_intensity))

    plot_intensity(mean_intensity)  #open it

    dt = 15 / 94
    times = np.arange(94) * dt

    plot_intensity_realtime(times, mean_intensity) #Open it)

    total_intn, max_intn, median =  Compute_tot_max(infile)
    
    plot_tot_max_median(total_intn, max_intn, median) #open it

    #print(f"tot: {total_intn} : max_intn : {max_intn} : median {median}")

    intensity_roi_mean = Auto_ROI_brightest_region(infile)
    time = np.arange(len(intensity_roi_mean))

    plot_auto_roi(time, intensity_roi_mean) #open it

    n_plots = 10

    vmin, vmax, data_intensity, indices  = Compute_intensity_timeframe(infile, 10)
    plot_xy_intensity(vmin, vmax, data_intensity, indices)

    


if __name__ == "__main__":
    main()


