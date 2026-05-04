import nd2
import numpy as np

#file_path = "/Users/tanmay/LenevoINFN/Work/BratatiImageJ/InFile/nd005.nd2"

mean_intensity = []

def ComputeMean():

    file_path = InputFile()
    with nd2.ND2File(file_path) as f:
        for i in range(f.sizes['T']):
            frame = f[i]   # load ONE frame only
            mean_intensity.append(frame.mean())

    mean_intensity = np.array(mean_intensity)
    return mean_intensity

intensity_asrry = []

def Compute_with_asrry():
   
    file_path = InputFile()
    with nd2.ND2File(file_path) as f:
        data = f.asarray()
    
    for i in range(data.shape[0]):
        frame = data[i]
        intensity_asrry.append(frame)

    return intensity_asrry

intensity_mean_asrry = []

def ComputeMean_with_asrry(file_path):

    with nd2.ND2File(file_path) as f:
        data = f.asarray()
    
    for i in range(data.shape[0]):
        frame = data[i]
        intensity_mean_asrry.append(frame.mean())

    return intensity_mean_asrry

def RealTime_Extract():

    file_path = InputFile()
    with nd2.ND2File(file_path) as f:
        if hasattr(f, "timestamps"):
            times = np.array(f.timestamps) / 60
        else:
            events = f.events()
            times = np.array([e.get("time", i) for i, e in enumerate(events)]) / 60

total_intensity = []
max_intensity = []
median_intensity = []  
def Compute_tot_max(file_path):

    with nd2.ND2File(file_path) as f:
        data = f.asarray()

    for i in range(data.shape[0]):
        frame = data[i]
        total_intensity.append(frame.sum())
        max_intensity.append(frame.max())
        median_intensity.append(np.median(frame))
        

    return total_intensity, max_intensity, median_intensity 

def Auto_ROI_brightest_region(file_path):

    with nd2.ND2File(file_path) as f:

        data = f.to_dask()   # lazy array
        print(data.shape)    # (94, 4656, 4656)
        first_frame = data[0].compute()

    # Find brightest pixel
    y, x = np.unravel_index(np.argmax(first_frame), first_frame.shape)

    # Define ROI size (adjustable)
    roi_size = 300

    y1 = max(0, y - roi_size//2)
    y2 = min(first_frame.shape[0], y + roi_size//2)

    x1 = max(0, x - roi_size//2)
    x2 = min(first_frame.shape[1], x + roi_size//2)

    auto_roi = (y1, y2, x1, x2)

    print("[DEBUG : ] Auto ROI:", auto_roi)

    mean_intensity_roi = []

    with nd2.ND2File(file_path) as f:
        data = f.to_dask()
        for i in range (f.sizes['T']):
            frame = data[i].compute() 
            roi = frame[y1:y2, x1:x2]
            mean_intensity_roi.append(roi.mean())

    mean_intensity_roi = np.array(mean_intensity_roi)

    return mean_intensity_roi

def Compute_intensity_timeframe(file_path, n_plots):

    # -----------------------------
    # INPUT
    # -----------------------------
    with nd2.ND2File(file_path) as f:
        data = f.to_dask()   # lazy loading
        T = f.sizes['T']

    print(f"[DEBUG : ] Total frames: {T}")
    indices = np.linspace(0, T - 1, n_plots, dtype=int)

    # -----------------------------
    # COMPUTE GLOBAL INTENSITY RANGE
    # (important for consistent plots)
    # -----------------------------
    sample_frames = [data[i].compute() for i in indices]
    stack = np.stack(sample_frames)

    vmin = np.percentile(stack, 1)
    vmax = np.percentile(stack, 99)

    #vmin = min(frame.min() for frame in sample_frames)
    #vmax = max(frame.max() for frame in sample_frames)

    print(f"[DEBUG : ] vmin : {vmin} : vmax : {vmax}")

    return vmin, vmax, data, indices 
