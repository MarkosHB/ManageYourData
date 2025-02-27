import os
import argparse
from manageyourdata.utils import constants
from manageyourdata.data_manager import DataManager


def validate_pdf_file(value: str): 
    if not value.endswith(".pdf"):
        raise argparse.ArgumentTypeError("The report file must have a '.pdf' extension.")
    return value


def main():
    # Initialize parser object.
    parser = argparse.ArgumentParser(
        description="ManageYourData is a tool for visualizing and analyzing files locally.",
        epilog=f"For support, visit {constants.GITHUB_URL}. Please report any bugs or feature requests."
    )

    # Define the mandatory argument of all ocurrences.
    group_ex = parser.add_mutually_exclusive_group(required=True)
    group_ex.add_argument("-f", "--file", type=str, help="Path to your data file in a supported file format.")
    group_ex.add_argument("-sf", "--supported-formats", action="store_true", help="Print the currently file format supported by the tool.")
    
    # Define the differents modes of the tool.
    group_in = parser.add_argument_group()
    group_in.add_argument("-r", "--report", type=validate_pdf_file, help="Generate a PDF report with the most relevant details.")
    group_in.add_argument("-e", "--export", choices=constants.FORMAT.keys(), help="Select a method to export your data unmodified.")
    
    args = parser.parse_args()
    
    if args.file:
        # Create DM object.
        dm = DataManager()
        # Fill with provided data.
        dm.load_data(args.file)

        if args.report:
            # Check if path to file save location is provided.
            dm.report_pdf(args.report if os.path.dirname(args.report) else f"reports/{args.report}")

        if args.export:
            dm.export_data(args.export)

    elif args.supported_formats:
        # Show aditional help about usage.
        print(f"Supported formats: {', '.join(constants.FORMAT.values())}")

    else:
        pass


if __name__ == "__main__":
    main()
