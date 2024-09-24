from potentiostat import Potentiostat
import matplotlib.pyplot as plt

port = 'COM11' #the name of the port on the computer
datafile = 'data.txt'
test_name = 'cyclic' #test_names = ['cyclic', 'sinusoid', 'constant', 'squareWave', 'linearSweep', 'chronoamp', 'multiStep']
curr_range = '1000uA' #curr_range_list = ['1uA', '10uA', '100uA', '1000uA']
sample_rate = 100  # Hz
volt_min = 0
volt_max = 1.5
volt_per_sec = 0.0001  # (V/s)
num_cycles = 5
amplitude = (volt_max - volt_min) / 2.0
offset = (volt_max + volt_min) / 2.0
period_ms = int(1000 * 4 * amplitude / volt_per_sec)
shift = 0.0
test_param = {
    'quietValue': 0.0,
    'quietTime': 0,
    'amplitude': amplitude,
    'offset': offset,
    'period': period_ms,
    'numCycles': num_cycles,
    'shift': shift,
}

try:
    dev = Potentiostat(port)
    print("Potentiostat initialized.")
    
    try:
        supported_ranges = dev.get_all_curr_range()
        print("Supported current ranges:", supported_ranges)
        
        if curr_range not in supported_ranges:
            print(f"Warning: Current range '{curr_range}' is not supported. Using default range.")
            curr_range = supported_ranges[-1] 
        
        dev.set_curr_range(curr_range)
        print(f"Current range set to {curr_range} successfully.")
    except Exception as e:
        print(f"Error with current range: {e}")
    
    dev.set_sample_rate(sample_rate)
    dev.set_param(test_name, test_param)

    t, volt, curr = dev.run_test(test_name, display='data', filename=datafile)

    plt.figure(1)
    plt.subplot(211)
    plt.plot(t, volt)
    plt.ylabel('Potential (V)')
    plt.grid(True)
    plt.subplot(212)
    plt.plot(t, curr)
    plt.ylabel('Current (uA)')
    plt.xlabel('Time (sec)')
    plt.grid(True)
    plt.savefig('plot_time_voltage_current.png')
    plt.close()
    plt.figure(2)
    plt.plot(volt, curr)
    plt.xlabel('Potential (V)')
    plt.ylabel('Current (uA)')
    plt.grid(True)
    plt.savefig('plot_voltage_current.png')
    plt.close()

except KeyError as e:
    print(f"KeyError: {e} - This hardware variant may not be supported or there is an issue with the current range settings.")
except Exception as e:
    print(f"Error: {e}")
