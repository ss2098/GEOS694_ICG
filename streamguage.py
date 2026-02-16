import numpy as np
import matplotlib.pyplot as plt
import os

class StreamGuage:
    """
    Class to represent and analyze USGS stream gauge data
    """
    def __init__(self, fid, station_id, station_name, starttime, units='ft'):
        self.fid = fid
        self.station_id = station_id
        self.station_name = station_name
        self.starttime = starttime
        self.units = units
        self.time = []
        self.data = np.array([]) 

    def read_guage_file(self):
        """
        Read gauge data from file and convert to minutes since start
        """
        # skip the header rows (28) as per USGS format
        date, time_str, hgt = np.loadtxt(self.fid, skiprows=28, usecols=[2, 3, 5],
                                       dtype=str).T
        hgt = hgt.astype(float)
        
        # get D, H, M to calculate total minutes
        days = [float(d[-2:]) for d in date]
        hours = [float(t.split(":")[0]) for t in time_str]
        mins = [float(t.split(":")[1]) for t in time_str]

        self.time = np.array([(d * 24 * 60) + (h * 60) + m for d, h, m in zip(days, hours, mins)])
        self.data = hgt
    
    def convert(self):
        """
        Convert height from feet to meters
        """
        self.data = self.data * 0.3048
        self.units = 'm'

    def demean(self):
        """
        Subtract the mean value from the data array
        """
        self.data = self.data - np.mean(self.data)

    def shift_time(self, offset):
        """
        Offset the time axis by a user-input amount of minutes
        """
        self.time = self.time + offset

    def plot(self, stage="Raw"):
        """
        Plot the stream gauge data and save the figure
        """
        if len(self.data) == 0:
            return
        
        # Check filename to label the plot correctly
        month_label = "September" if "09-07" in self.fid else "October"
        
        plt.figure(figsize=(10, 5))
        plt.plot(self.time, self.data, 'b-', linewidth=1)
        plt.xlabel('Time (minutes since start of month)')
        plt.ylabel(f'Gauge Height ({self.units})')
        plt.title(f'{month_label} Data - {stage}\nStation: {self.station_name} ({self.units})')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save the plot automatically for GitHub documentation
        file_name = f"{month_label}_{stage.replace(' ', '_')}.png"
        plt.savefig(file_name)
        print(f"Saved plot: {file_name}")
        
        plt.show()

    def main(self):
        """
        Run the full processing and plotting pipeline (Tasks 3.4, 5, & 6)
        """
        self.read_guage_file()
        self.plot(stage="Initial")
        self.convert()
        self.demean()
        self.shift_time(-100)
        self.plot(stage="Processed")



class NOAAStreamgauge(StreamGuage):
    """
    Task 6: Child class for NOAA gauges that are already in meters
    """
    units = 'm'
    
    def convert(self):
        """
        Overwrite convert because NOAA is already in meters
        """
        pass

    def read_guage_file(self):
        """
        Call parent read function and print identity using super()
        """
        super().read_guage_file()
        print("I am a NOAA stream gauge")



if __name__ == "__main__":
    # Define data files (Task 5)
    sept_file = "phelan_creek_stream_guage_2024-09-07_to_2024-09-14.txt"
    oct_file = "phelan_creek_stream_gauge_2024-10-07_to_2024-10-14.txt"

    # Set up the loop to handle both USGS and NOAA gauges (Task 5 & 6)
    # This uses a list of tuples: (file_path, Class_to_use)
    gauge_list = [
        (sept_file, NOAAStreamgauge), 
        (oct_file, StreamGuage)
    ]
    
    for fid, GaugeClass in gauge_list:
        if os.path.exists(fid):
            print(f"\n--- Starting Pipeline for: {fid} ---")
            # Create the object using whichever class is in the list
            sg = GaugeClass(fid, "15478040", "PHELAN CREEK", "2024-XX-07")
            # Run the main processing method
            sg.main()
        else:
            print(f"File {fid} not found, skipping.")
