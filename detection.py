import numpy as np
from gpiozero import Buzzer
import time

def detect_ecoli(absorbance, wavelength):
    # Detect if the maximum peak wavelength is 275 nm
    max_peak_index = np.argmax(absorbance)
    max_peak_wavelength = wavelength[max_peak_index]
    if max_peak_wavelength == 275:
        return True
    else:
        return False

def detect_mrsa(absorbance, wavelength):
    # Detect if peaks are present at 1220 nm and 1080 nm
    peak_indices = np.where((wavelength == 1220) | (wavelength == 1080))[0]
    if len(peak_indices) == 2:
        return True
    else:
        return False

def calculate_concentration(absorbance, path_length, extinction_coefficient):
    # Calculate concentration based on Beer-Lambert Law
    concentration = absorbance / (extinction_coefficient * path_length)
    return concentration

def send_signal_to_raspberry_pi():
    # Send a signal to beep the Raspberry Pi
    buzzer = Buzzer(17) 
    buzzer.beep(on_time=0.5, off_time=0.5, n=3)
    buzzer.close()

# Continuous stream of absorbance measurements
absorbance_stream = [0.5, 0.6, 0.7, 0.8]
wavelengths = np.array([1080, 1120, 1220, 1250])  
extinction_coefficient_ecoli = 5000  
extinction_coefficient_mrsa = 6000  

for absorbance in absorbance_stream:
    if detect_ecoli(absorbance, wavelengths):
        concentration_ecoli = calculate_concentration(absorbance, 1, extinction_coefficient_ecoli) 
        if concentration_ecoli > 70:
            send_signal_to_raspberry_pi()
            print("High E. coli concentration detected! Beeping Raspberry Pi.")
        else:
            print("E. coli concentration is below threshold.")
    elif detect_mrsa(absorbance, wavelengths):
        concentration_mrsa = calculate_concentration(absorbance, 1, extinction_coefficient_mrsa) 
        if concentration_mrsa > 70:
            send_signal_to_raspberry_pi()
            print("High MRSA concentration detected! Beeping Raspberry Pi.")
        else:
            print("MRSA concentration is below threshold.")
    else:
        print("No E. coli or MRSA detected.")
    # Simulating continuous stream with a delay of 1 second
    time.sleep(1)  
