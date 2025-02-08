import matplotlib.pyplot as plt

def filter_lines_by_ids(input_file, output_file, valid_ids):
    """
    Filters lines in the input file based on the given valid IDs, removes duplicates, and writes the result to the output file.
    
    :param input_file: Path to the input file containing data.
    :param output_file: Path to save the filtered data.
    :param valid_ids: A set of IDs to keep in the output.
    """
    seen_lines = set()
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            parts = line.split(', ')
            for part in parts:
                if part.startswith("ID: "):
                    id_value = int(part.split()[1])
                    if id_value in valid_ids and line not in seen_lines:
                        outfile.write(line)
                        seen_lines.add(line)
                    break

def plot_yaw_data(input_file):
    """
    Reads the filtered file and creates a (2,1) subplot of yaw and 3D yaw vs time.
    
    :param input_file: Path to the input file containing the filtered data.
    """
    times, yaws, yaw_3ds = [], [], []
    
    with open(input_file, 'r') as infile:
        for line in infile:
            parts = line.split(', ')
            time = float(parts[0].split(': ')[1])
            yaw = float(parts[2].split(': ')[1])
            yaw_3d = float(parts[3].split(': ')[1])
            
            times.append(time)
            yaws.append(yaw)
            yaw_3ds.append(yaw_3d)
    
    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    axs[0].scatter(times, yaws, label='Tracker Yaw', color='b', s=6)
    axs[0].set_ylabel('Yaw')
    axs[0].legend()
    axs[0].set_ylim(-7, 7)
    axs[0].grid()
    
    axs[1].scatter(times, yaw_3ds, label='3D Yaw', color='r', s=6)
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('3D Yaw')
    axs[1].set_ylim(-7, 7)
    axs[1].legend()
    axs[1].grid()
    
    axs
    plt.show()

if __name__ == "__main__":
    # Prompt user for valid IDs
    input_ids = input("Enter IDs to keep, separated by spaces: ")
    valid_ids = set(map(int, input_ids.split()))
    
    input_filename = "/home/yang/output/yaw_output.txt"  # Replace with your actual input file
    output_filename = "/home/yang/output/filtered_yaw_output.txt"  # Replace with your desired output file
    
    filter_lines_by_ids(input_filename, output_filename, valid_ids)
    print(f"Filtered data saved to {output_filename}")
    
    plot_yaw_data(output_filename)
