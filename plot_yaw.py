import matplotlib.pyplot as plt

def load_valid_ids(id_file):
    """
    Loads valid IDs from a text file, ensuring all IDs are read correctly.
    
    :param id_file: Path to the file containing IDs.
    :return: A set of valid IDs.
    """
    valid_ids = set()
    try:
        with open(id_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    valid_ids.update(map(int, line.split()))  # Handles multiple IDs in one line
    except FileNotFoundError:
        print(f"Error: File {id_file} not found.")
    print(f"Loaded valid IDs: {valid_ids}")  # Debugging output
    return valid_ids

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
    axs[0].set_ylabel('Tracker Yaw')
    axs[0].set_ylim(-6, 6)
    axs[0].legend()
    axs[0].grid()
    
    axs[1].scatter(times, yaw_3ds, label='3D Yaw', color='r', s=6)
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('3D Yaw')
    axs[1].set_ylim(-6, 6)
    axs[1].legend()
    axs[1].grid()
    fig.suptitle(f"Bag name: {title_name}")
    fig.savefig(f"/home/yang/output/images/{title_name}_yaw_plot.png", dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    title_name = input("Please type name of the bag: ")
    print(title_name)
    id_filename = "/home/yang/output/valid_ids.txt"  
    input_filename = "/home/yang/output/yaw_output.txt"  
    output_filename = "/home/yang/output/filtered_yaw_output.txt" 
    
    valid_ids = load_valid_ids(id_filename)
    if not valid_ids:
        print("Warning: No valid IDs were loaded. Check the format of your ID file.")
    filter_lines_by_ids(input_filename, output_filename, valid_ids)
    print(f"Filtered data saved to {output_filename}")
    
    plot_yaw_data(output_filename)
