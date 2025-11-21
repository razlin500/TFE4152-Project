import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
from PIL import Image


def setup_plot_style():
    """Configure matplotlib for visually appealing plots."""
    # Try to use seaborn style, fallback to default if not available
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except:
        try:
            plt.style.use('seaborn-darkgrid')
        except:
            plt.style.use('default')
    
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['savefig.bbox'] = 'tight'


def read_and_split_data(file_path):
    """
    Read data from a file and split it into separate experiments.
    
    Args:
        file_path: Path to the data file
        
    Returns:
        DataFrame with columns: sweep, id_exp1, id_exp2, id_exp3
    """
    data = pd.read_table(file_path)
    
    # Find where each experiment starts (when sweep resets to 0)
    sweep_col = data.columns[0]  # First sweep column
    id_col = data.columns[2]      # id(m1a) column
    
    # Find experiment boundaries by detecting when sweep resets to 0
    experiment_starts = [0]  # Start with first data row
    for i in range(1, len(data)):
        if abs(data.iloc[i][sweep_col]) < 1e-10:  # Check if sweep is approximately 0
            experiment_starts.append(i)
    
    # Ensure we have exactly 3 experiments
    if len(experiment_starts) < 3:
        # If we didn't find enough resets, assume equal division
        rows_per_experiment = len(data) // 3
        experiment_starts = [0, rows_per_experiment, 2 * rows_per_experiment]
    else:
        experiment_starts = experiment_starts[:3]  # Take first 3 experiments
    
    # Add the end index for the last experiment
    experiment_starts.append(len(data))
    
    # Extract each experiment's data
    exp1_data = data.iloc[experiment_starts[0]:experiment_starts[1]][id_col].values
    exp2_data = data.iloc[experiment_starts[1]:experiment_starts[2]][id_col].values
    exp3_data = data.iloc[experiment_starts[2]:experiment_starts[3]][id_col].values
    
    # Get the common sweep values (from first experiment)
    sweep_values = data.iloc[experiment_starts[0]:experiment_starts[1]][sweep_col].values
    
    # Ensure all experiments have the same length (take minimum length)
    min_length = min(len(exp1_data), len(exp2_data), len(exp3_data))
    sweep_values = sweep_values[:min_length]
    exp1_data = exp1_data[:min_length]
    exp2_data = exp2_data[:min_length]
    exp3_data = exp3_data[:min_length]
    
    # Create new DataFrame with 4 columns: sweep, id_exp1, id_exp2, id_exp3
    split_data = pd.DataFrame({
        'sweep': sweep_values,
        'id_exp1': exp1_data,
        'id_exp2': exp2_data,
        'id_exp3': exp3_data
    })
    
    return split_data


def read_iin_data(file_path):
    """
    Read data from an _Iin file.
    Note: The file has duplicate sweep columns, we use the first one.
    
    Args:
        file_path: Path to the _Iin data file
        
    Returns:
        DataFrame with columns: sweep_current, id_current
    """
    data = pd.read_table(file_path)
    
    # Use first sweep column (column 0) and id(m1a) column (column 2)
    # Ignore the duplicate sweep column (column 1)
    sweep_col = data.columns[0]  # First sweep column (input current)
    id_col = data.columns[2]      # id(m1a) column (drain current)
    
    return pd.DataFrame({
        'sweep_current': data[sweep_col].values,
        'id_current': data[id_col].values
    })


def plot_voltage_sweep(split_data, output_path, process, voltage_offset, temperature):
    """
    Plot voltage sweep data for all three experiments.
    
    Args:
        split_data: DataFrame with columns: sweep, id_exp1, id_exp2, id_exp3
        output_path: Path to save the plot
        process: Process type (ss, tt, ff)
        voltage_offset: Voltage offset (0, 01, 10)
        temperature: Temperature (0, 27, 50)
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot all three experiments
    ax.plot(split_data['sweep'], split_data['id_exp1'], 
            label='Iin = 40 μA', linewidth=2, alpha=0.8)
    ax.plot(split_data['sweep'], split_data['id_exp2'], 
            label='Iin = 45 μA', linewidth=2, alpha=0.8)
    ax.plot(split_data['sweep'], split_data['id_exp3'], 
            label='Iin = 50 μA', linewidth=2, alpha=0.8)
    
    # Add horizontal reference lines at 40 uA, 45 uA, and 50 uA
    reference_currents = [40e-6, 45e-6, 50e-6]  # Convert to Amperes
    reference_labels = ['40 μA', '45 μA', '50 μA']
    
    for current, label in zip(reference_currents, reference_labels):
        ax.axhline(y=current, color='gray', linestyle=':', linewidth=1.5, 
                  alpha=0.7, zorder=0)  # zorder=0 to place behind data lines
    
    # Format labels
    ax.set_xlabel('Voltage sweep [V]', fontweight='bold')
    ax.set_ylabel('Drain current M1 [A]', fontweight='bold')
    
    # Create title with file information
    voltage_str = f"{voltage_offset}" if voltage_offset != "01" else "-10%"
    if voltage_offset == "10":
        voltage_str = "+10%"
    elif voltage_offset == "0":
        voltage_str = "0%"
    
    title = f"Process: {process.upper()}, Voltage: {voltage_str}, Temperature: {temperature}°C"
    ax.set_title(title, fontweight='bold', pad=15)
    
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Improve layout
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot: {output_path}")


def plot_current_error(iin_data, output_path, process, voltage_offset, temperature):
    """
    Plot absolute error squared between sweep current and drain current.
    For each row: (sweep_current - id_current)^2, plotted against sweep_current.
    Averages every 10 entries in id_current to reduce data points from ~1400 to ~140.
    
    Args:
        iin_data: DataFrame with columns: sweep_current, id_current
        output_path: Path to save the plot
        process: Process type (ss, tt, ff)
        voltage_offset: Voltage offset (0, 01, 10)
        temperature: Temperature (0, 27, 50)
    """
    # Convert to numpy arrays
    sweep_current = np.array(iin_data['sweep_current'], dtype=np.float64)
    id_current = np.array(iin_data['id_current'], dtype=np.float64)
    
    # Average every 10 entries in id_current
    chunk_size = 10
    n_chunks = len(id_current) // chunk_size
    
    # Reshape and average id_current in chunks of 10
    id_current_reshaped = id_current[:n_chunks * chunk_size].reshape(n_chunks, chunk_size)
    id_current_averaged = np.mean(id_current_reshaped, axis=1)
    
    # Take corresponding sweep_current values (first value of each chunk)
    sweep_current_averaged = sweep_current[::chunk_size][:n_chunks]
    
    # Calculate error: (sweep_current - id_current)
    error_squared = np.abs(sweep_current_averaged - id_current_averaged)

    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot error squared against sweep current
    ax.plot(sweep_current_averaged, error_squared, 
            linewidth=1, color='red', alpha=0.8, label='Data')
    
    # Fit a polynomial trendline (degree 2 for smooth curve)
    z = np.polyfit(sweep_current_averaged, error_squared, deg=2)
    p = np.poly1d(z)
    
    # Create smooth x values for trendline
    sweep_smooth = np.linspace(sweep_current_averaged.min(), 
                               sweep_current_averaged.max(), 200)
    trendline = p(sweep_smooth)
    
    # Plot trendline
    ax.plot(sweep_smooth, trendline, 
            linewidth=2.5, color='blue', alpha=0.9, 
            linestyle='-', label='Trendline')
    
    # Format labels
    ax.set_xlabel('Input Current [A]', fontweight='bold')
    ax.set_ylabel('Absolute Error', fontweight='bold')
    
    # Create title with file information
    voltage_str = f"{voltage_offset}" if voltage_offset != "01" else "-10%"
    if voltage_offset == "10":
        voltage_str = "+10%"
    elif voltage_offset == "0":
        voltage_str = "0%"
    
    title = f"Current Error |Iin - Iout| - Process: {process.upper()}, Voltage: {voltage_str}, Temperature: {temperature}°C"
    ax.set_title(title, fontweight='bold', pad=15)
    
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Use scientific notation for y-axis if needed
    ax.ticklabel_format(style='scientific', axis='y', scilimits=(0, 0))
    ax.ticklabel_format(style='scientific', axis='x', scilimits=(0, 0))
    
    # Improve layout
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot: {output_path}")


def plot_combined_error_trendlines(iin_files, plots_dir, results_dir):
    """
    Create a combined plot with trendlines from all _Iin error plots.
    Only shows the interpolated trendlines, not the raw data.
    
    Args:
        iin_files: List of paths to _Iin files
        plots_dir: Directory to save the combined plot
        results_dir: Directory containing result files (for finding files)
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Color palette for different conditions
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    color_idx = 0
    
    for file_path in iin_files:
        process, voltage_offset, temperature, is_iin = parse_filename(file_path)
        if process is None:
            continue
        
        try:
            # Read data
            iin_data = read_iin_data(file_path)
            
            # Convert to numpy arrays
            sweep_current = np.array(iin_data['sweep_current'], dtype=np.float64)
            id_current = np.array(iin_data['id_current'], dtype=np.float64)
            
            # Average every 10 entries in id_current
            chunk_size = 10
            n_chunks = len(id_current) // chunk_size
            
            # Reshape and average id_current in chunks of 10
            id_current_reshaped = id_current[:n_chunks * chunk_size].reshape(n_chunks, chunk_size)
            id_current_averaged = np.mean(id_current_reshaped, axis=1)
            
            # Take corresponding sweep_current values (first value of each chunk)
            sweep_current_averaged = sweep_current[::chunk_size][:n_chunks]
            
            # Calculate error: (sweep_current - id_current)
            error_squared = np.abs(sweep_current_averaged - id_current_averaged)
            
            # Fit a polynomial trendline (degree 2 for smooth curve)
            z = np.polyfit(sweep_current_averaged, error_squared, deg=2)
            p = np.poly1d(z)
            
            # Create smooth x values for trendline
            sweep_smooth = np.linspace(sweep_current_averaged.min(), 
                                       sweep_current_averaged.max(), 200)
            trendline = p(sweep_smooth)
            
            # Create label
            voltage_str = f"{voltage_offset}" if voltage_offset != "01" else "-10%"
            if voltage_offset == "10":
                voltage_str = "+10%"
            elif voltage_offset == "0":
                voltage_str = "0%"
            
            label = f"{process.upper()}, {voltage_str}, {temperature}°C"
            
            # Plot trendline only
            ax.plot(sweep_smooth, trendline, 
                    linewidth=2, color=colors[color_idx % len(colors)], 
                    alpha=0.8, label=label)
            
            color_idx += 1
            
        except Exception as e:
            print(f"Error processing {file_path} for combined plot: {e}")
    
    # Format labels
    ax.set_xlabel('Input Current [A]', fontweight='bold')
    ax.set_ylabel('Absolute Error[A]', fontweight='bold')
    ax.set_title('Current Error = |Iin - Iout| - Combined Trendlines', fontweight='bold', pad=15)
    
    ax.legend(loc='best', framealpha=0.9, fontsize=9)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Use scientific notation for axes
    ax.ticklabel_format(style='scientific', axis='y', scilimits=(0, 0))
    ax.ticklabel_format(style='scientific', axis='x', scilimits=(0, 0))
    
    # Improve layout
    plt.tight_layout()
    
    # Save combined plot
    output_path = os.path.join(plots_dir, 'combined_error_trendlines.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Saved combined error plot: {output_path}")


def find_result_files(results_dir):
    """
    Find all result files matching the pattern xx_yy_zz.txt.
    
    Args:
        results_dir: Directory containing result files
        
    Returns:
        Tuple of (regular_files, iin_files) where each is a list of file paths
    """
    pattern = re.compile(r'^(ss|tt|ff)_(0|01|10)_(0|27|50)$')
    iin_pattern = re.compile(r'^(ss|tt|ff)_(0|01|10)_(0|27|50)_Iin$')
    
    regular_files = []
    iin_files = []
    
    for file in os.listdir(results_dir):
        file_path = os.path.join(results_dir, file)
        if os.path.isfile(file_path) and not file.endswith('.txt'):
            # Try without extension
            base_name = file
            if pattern.match(base_name):
                regular_files.append(file_path)
            elif iin_pattern.match(base_name):
                iin_files.append(file_path)
    
    return regular_files, iin_files


def parse_filename(file_path):
    """
    Parse filename to extract process, voltage offset, and temperature.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Tuple of (process, voltage_offset, temperature, is_iin)
    """
    filename = os.path.basename(file_path)
    is_iin = filename.endswith('_Iin') or '_Iin' in filename
    
    if is_iin:
        match = re.match(r'^(ss|tt|ff)_(0|01|10)_(0|27|50)_Iin$', filename)
    else:
        match = re.match(r'^(ss|tt|ff)_(0|01|10)_(0|27|50)$', filename)
    
    if match:
        return match.group(1), match.group(2), match.group(3), is_iin
    return None, None, None, is_iin


def main():
    """Main function to process all result files and generate plots."""
    # Setup
    setup_plot_style()
    current_path = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(current_path, 'results')
    plots_dir = os.path.join(current_path, 'plots')
    
    # Create plots directory if it doesn't exist
    os.makedirs(plots_dir, exist_ok=True)
    
    # Find all result files
    regular_files, iin_files = find_result_files(results_dir)
    
    print(f"Found {len(regular_files)} regular files and {len(iin_files)} _Iin files")
    
    # Process regular files
    for file_path in regular_files:
        process, voltage_offset, temperature, is_iin = parse_filename(file_path)
        if process is None:
            continue
        
        try:
            # Read and split data
            split_data = read_and_split_data(file_path)
            
            # Create output filename
            filename = os.path.basename(file_path)
            output_filename = f"{filename}_plot.png"
            output_path = os.path.join(plots_dir, output_filename)
            
            # Plot
            plot_voltage_sweep(split_data, output_path, process, voltage_offset, temperature)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    # Process _Iin files - create combined plot with trendlines only
    if iin_files:
        plot_combined_error_trendlines(iin_files, plots_dir, results_dir)
    
    print(f"\nAll plots saved to: {plots_dir}")
    
    # Merge all plots into a single PDF
    merge_plots_to_pdf(plots_dir)
    
    # Generate comprehensive metrics table
    generate_metrics_table(results_dir, plots_dir)


def merge_plots_to_pdf(plots_dir):
    """
    Merge all PNG plot images in the plots directory into a single PDF file.
    
    Args:
        plots_dir: Directory containing the plot images
    """
    # Find all PNG files in the plots directory
    plot_files = [f for f in os.listdir(plots_dir) if f.endswith('.png')]
    
    if not plot_files:
        print("No plot files found to merge.")
        return
    
    # Sort files: regular plots first, then _Iin error plots
    # Sort by filename to ensure consistent ordering
    plot_files.sort()
    
    # Separate regular plots and error plots for better organization
    regular_plots = [f for f in plot_files if '_Iin' not in f]
    error_plots = [f for f in plot_files if '_Iin' in f]
    
    # Combine: regular plots first, then error plots
    sorted_plots = regular_plots + error_plots
    
    # Create PDF path
    pdf_path = os.path.join(plots_dir, 'all_plots.pdf')
    
    try:
        # Open all images and convert to RGB (required for PDF)
        images = []
        for plot_file in sorted_plots:
            img_path = os.path.join(plots_dir, plot_file)
            img = Image.open(img_path)
            # Convert to RGB if necessary (PNG might have RGBA)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)
        
        # Save as PDF (first image determines size, others will be resized to fit)
        if images:
            # Use the first image's size as the base
            first_image = images[0]
            # Save all images as pages in PDF
            first_image.save(
                pdf_path,
                "PDF",
                resolution=100.0,
                save_all=True,
                append_images=images[1:] if len(images) > 1 else []
            )
            print(f"\nMerged {len(images)} plots into: {pdf_path}")
        else:
            print("No valid images found to merge.")
            
    except Exception as e:
        print(f"Error merging plots to PDF: {e}")
        # Fallback: try using matplotlib's PdfPages
        try:
            from matplotlib.backends.backend_pdf import PdfPages
            with PdfPages(pdf_path) as pdf:
                for plot_file in sorted_plots:
                    img_path = os.path.join(plots_dir, plot_file)
                    img = Image.open(img_path)
                    # Convert to numpy array for matplotlib
                    img_array = np.array(img.convert('RGB'))
                    fig, ax = plt.subplots(figsize=(12, 8))
                    ax.imshow(img_array)
                    ax.axis('off')
                    pdf.savefig(fig, bbox_inches='tight', pad_inches=0)
                    plt.close(fig)
            print(f"\nMerged {len(sorted_plots)} plots into: {pdf_path}")
        except Exception as e2:
            print(f"Error with matplotlib PDF backend: {e2}")


def get_vdd_value(voltage_offset):
    """Convert voltage offset string to actual V_DD value."""
    if voltage_offset == "01":
        return "0.9V"  # -10%
    elif voltage_offset == "10":
        return "1.1V"  # +10%
    else:
        return "1.0V"  # nominal (0)


def get_vdd_numeric(voltage_offset):
    """Convert voltage offset string to numeric V_DD value."""
    if voltage_offset == "01":
        return 0.9  # -10%
    elif voltage_offset == "10":
        return 1.1  # +10%
    else:
        return 1.0  # nominal (0)


def interpolate_value(x_data, y_data, target_x):
    """Interpolate y value at target_x from x_data and y_data."""
    # Find the closest points
    idx = np.searchsorted(x_data, target_x)
    
    if idx == 0:
        return y_data[0]
    elif idx >= len(x_data):
        return y_data[-1]
    else:
        # Linear interpolation
        x1, x2 = x_data[idx-1], x_data[idx]
        y1, y2 = y_data[idx-1], y_data[idx]
        return y1 + (y2 - y1) * (target_x - x1) / (x2 - x1)


def calculate_error_percentage(iin_file_path, target_iin):
    """
    Calculate error percentage from Iin file for a specific input current.
    
    Args:
        iin_file_path: Path to the _Iin file
        target_iin: Target input current in Amperes (e.g., 40e-6)
        
    Returns:
        Error percentage
    """
    try:
        iin_data = read_iin_data(iin_file_path)
        sweep_current = np.array(iin_data['sweep_current'], dtype=np.float64)
        id_current = np.array(iin_data['id_current'], dtype=np.float64)
        
        # Find closest sweep current to target
        idx = np.argmin(np.abs(sweep_current - target_iin))
        
        if idx < len(sweep_current):
            i_sweep = sweep_current[idx]
            i_drain = id_current[idx]
            
            if abs(i_sweep) > 1e-10:  # Avoid division by zero
                error_pct = abs((i_sweep - i_drain) / i_sweep) * 100
                return error_pct
        
        return 0.0
    except:
        return 0.0


def generate_metrics_table(results_dir, plots_dir):
    """
    Generate a comprehensive table with key metrics from all 27 simulations.
    
    Args:
        results_dir: Directory containing result files
        plots_dir: Directory to save the output table
    """
    # Find all regular result files
    regular_files, _ = find_result_files(results_dir)
    
    # Input currents for the three experiments
    iin_values = [40e-6, 45e-6, 50e-6]  # 40µA, 45µA, 50µA
    iin_labels = ["40µA", "45µA", "50µA"]
    
    # Store all metrics
    table_data = []
    
    for file_path in regular_files:
        process, voltage_offset, temperature, is_iin = parse_filename(file_path)
        if process is None:
            continue
        
        try:
            # Read and split data
            split_data = read_and_split_data(file_path)
            
            # Get V_DD value
            vdd_str = get_vdd_value(voltage_offset)
            vdd_num = get_vdd_numeric(voltage_offset)
            
            # Process each of the three experiments
            for exp_idx, (iin_val, iin_label) in enumerate(zip(iin_values, iin_labels)):
                # Get experiment data
                if exp_idx == 0:
                    current_data = split_data['id_exp1'].values
                elif exp_idx == 1:
                    current_data = split_data['id_exp2'].values
                else:
                    current_data = split_data['id_exp3'].values
                
                voltage_data = split_data['sweep'].values
                
                # Find V_out,min: lowest voltage where I_out is within 1% of I_in
                # I_out should be between 0.99 * I_in and 1.01 * I_in
                lower_bound = 0.99 * iin_val
                upper_bound = 1.01 * iin_val
                
                # Find indices where current is within 1% of I_in
                within_range = np.where((current_data >= lower_bound) & (current_data <= upper_bound))[0]
                
                if len(within_range) > 0:
                    v_out_min = voltage_data[within_range[0]]  # First (lowest) voltage where condition is met
                else:
                    # If no exact match, find closest
                    diff = np.abs(current_data - iin_val)
                    closest_idx = np.argmin(diff)
                    v_out_min = voltage_data[closest_idx]
                
                # Find I_out @ V_out=0.9V (interpolate)
                i_out_09v = interpolate_value(voltage_data, current_data, 0.9)
                
                # Calculate power: P = (50 + 35 + I_out @ V_out) * 0.9
                # Where 50 and 35 are in µA, I_out is in µA, 0.9 is voltage in V
                i_out_09v_ua = i_out_09v * 1e6  # Convert to µA
                power_uw = (50 + 35 + i_out_09v_ua) * 0.9  # Result in µW
                
                # Add row to table
                table_data.append({
                    'Process': process.upper(),
                    'V_DD': vdd_str,
                    'Temp': f"{temperature}°C",
                    'I_in': iin_label,
                    'V_out,min': f"{v_out_min:.3f}V",
                    'I_out @ V_out=0.9V': f"{i_out_09v*1e6:.2f}µA",
                    'Power': f"{power_uw:.2f}µW"
                })
                
        except Exception as e:
            print(f"Error processing {file_path} for metrics: {e}")
    
    # Create DataFrame
    df = pd.DataFrame(table_data)
    
    # Sort by Process, V_DD, Temp, I_in
    df['Process_order'] = df['Process'].map({'SS': 1, 'TT': 2, 'FF': 3})
    df['V_DD_order'] = df['V_DD'].map({'0.9V': 1, '1.0V': 2, '1.1V': 3})
    df['Temp_order'] = df['Temp'].str.extract(r'(\d+)').astype(float)
    df['I_in_order'] = df['I_in'].str.extract(r'(\d+)').astype(float)
    
    df = df.sort_values(['Process_order', 'V_DD_order', 'Temp_order', 'I_in_order'])
    df = df.drop(['Process_order', 'V_DD_order', 'Temp_order', 'I_in_order'], axis=1)
    
    # Save to CSV
    csv_path = os.path.join(plots_dir, 'simulation_metrics.csv')
    df.to_csv(csv_path, index=False)
    print(f"\nMetrics table saved to: {csv_path}")
    
    # Also create a formatted text table
    txt_path = os.path.join(plots_dir, 'simulation_metrics.txt')
    with open(txt_path, 'w') as f:
        f.write("Comprehensive Table: Key Metrics from All 27 Simulations\n")
        f.write("=" * 120 + "\n\n")
        f.write(df.to_string(index=False))
        f.write("\n")
    print(f"Formatted table saved to: {txt_path}")
    
    # Print summary
    print(f"\nTotal rows in table: {len(df)}")
    print("\nFirst few rows:")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()