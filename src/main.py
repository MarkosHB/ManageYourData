import os
import argparse
from utils import constants
from data_manager import DataManager


def validate_pdf_file(value: str): 
    if not value.endswith(".pdf"):
        raise argparse.ArgumentTypeError("The report file must have a '.pdf' extension.")
    return value


def main():
    # Initialize parser object.
    parser = argparse.ArgumentParser(
        description="ManageYourData is a tool for visualizing and analyzing files locally.",
        epilog="For support, visit 'https://github.com/MarkosHB/ManageYourData'. Please report any bugs or feature requests."
    )

    # Define the mandatory argument of all ocurrences.
    parser.add_argument("-f", "--file", required=True, type=str, help="Path to your data file in a supported file format.")
    
    # Define the differents modes of the tool.
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-sf", "--supported-formats", action="store_true", help="Print the currently file format supported by the tool.")
    group.add_argument("-r", "--report", type=validate_pdf_file, help="Generate a PDF report with the most relevant details.")
    group.add_argument("-e", "--export", choices=constants.FORMAT.keys(), help="Select a method to export your data unmodified.")
    
    args = parser.parse_args()

    # Create DM object.
    dm = DataManager()
    # Fill with provided data.
    dm.load_data(args.file)
    
    # Discern between functionalities.
    if args.supported_formats:
        print(f"Supported formats: {', '.join(constants.FORMAT.values())}")
    
    elif args.report:
        # Check if path is provided.
        dm.report_pdf(args.report if os.path.dirname(args.report) else f"reports/{args.report}")

    elif args.export:
        dm.export_data(f"exports/{args.export}")

    else:
        pass


if __name__ == "__main__":
    main()
