#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import sys
import textwrap
try:
    import pandas as pd
except ModuleNotFoundError:
    print("Error: lib not found, please install it using 'conda install conda-forge::pandas'")
    sys.exit()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Filter sequences based on coverage threshold.")
    parser.add_argument("-d", "--depth", 
                        required=True, 
                        help="Path to the depth.txt file")
    parser.add_argument("-c", "--consensus", 
                        required=True, 
                        help="Path to the draft_consensus.fasta file")
    parser.add_argument("-t", "--treshold", 
                        required=True, 
                        type=int, 
                        help='A required trash coverage level int')
    parser.add_argument("-o", "--output_dir", 
                        required=False, 
                        help="Path to the output directory where filtered_cons.fasta will be saved")
    return parser.parse_args()


def filter_sequences(depth_file, cons_file, treshold, output_dir):
    # Read the depth.txt into a DataFrame
    depth = pd.read_csv(depth_file, engine='python', sep="\\s+", names=["SEG_NAME", "POS", "COVERAGE"])

    # Calculate average coverage for each unique SEG_NAME
    result = depth.groupby("SEG_NAME")["COVERAGE"].mean().reset_index()
    result.rename(columns={"COVERAGE": "AV_COVERAGE"}, inplace=True)

    # Filter the result DataFrame based on the threshold
    filtered_result = result[result['AV_COVERAGE'] >= treshold]
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Define the output file path
    output_file = os.path.join(output_dir, "filtered_cons.fasta")

    # Open the input and output files
    with open(cons_file, "r") as infile, open(output_file, "w") as outfile:
        current_header = None
        current_sequence = ""

        # Iterate over each line in the input file
        for line in infile:
            line = line.strip()  # Remove leading/trailing whitespace

            # Check if the line is a header line
            if line.startswith(">"):
                # Check if the current sequence belongs to one of the filtered SEG_NAME values
                if current_header in filtered_result["SEG_NAME"].values:
                    # Write the current header and sequence to the output file
                    formatted_sequence = "\n".join(textwrap.wrap(current_sequence, 60))
                    outfile.write(f">{current_header}\n{formatted_sequence}\n")

                # Reset the current sequence and update the current header
                current_sequence = ""
                current_header = line[1:]  # Remove the ">" character

            else:
                # Accumulate the sequence
                current_sequence += line

        # Write the last sequence if it belongs to one of the filtered SEG_NAME values
        if current_header in filtered_result["SEG_NAME"].values:
            # print(current_header)
            formatted_sequence = "\n".join(textwrap.wrap(current_sequence, 60))
            outfile.write(f">{current_header}\n{formatted_sequence}\n")

    # Return the path to the output file
    return output_file


def main():
    #Parse command line arguments
    args = parse_arguments()

    # If output directory is not provided, use current directory
    output_dir = args.output_dir if args.output_dir else os.getcwd()

    # Filter sequences based on coverage threshold
    output_file = filter_sequences(args.depth, args.consensus, args.treshold, output_dir)
 
    # Confirmation message
    #print(f"Filtered consensus has been saved to {output_dir}{output_file}")


if __name__ == "__main__":
    main()
