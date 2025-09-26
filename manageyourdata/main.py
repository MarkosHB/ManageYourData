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
    group_ex.add_argument("-ap", "--available_providers", action="store_true", help="Print the currently available AI llm's providers.")
    
    # Define the differents modes of the tool.
    group_in = parser.add_argument_group()
    group_in.add_argument("-r", "--report", type=validate_pdf_file, help="Generate a PDF report with the most relevant details.")
    group_in.add_argument("-e", "--export", choices=constants.FORMAT.keys(), help="Select a method to export your data unmodified.")
    group_in.add_argument("-c", "--chat", action="store_true", help="Interact with your data using AI.")

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

        if args.chat:
            provider = input("Insert your desired AI provider: ").strip()
            model = input("Insert the actual name of the model: ").strip()
            api_key = input("Insert your API key (if needed, else press enter): ").strip() or None

            dm.create_assistant(provider, model, api_key)
            while True:
                prompt = input("You: ").strip()
                if prompt.lower() in ["exit", "quit", "q"]:
                    print("Exiting the chat. Goodbye!")
                    break
                try:
                    response = dm.chat_with_assistant(prompt)
                    print(f"AI: {response}")
                except Exception as e:
                    print(f"Error: {e}")

    elif args.supported_formats:
        # Show aditional help about usage.
        print(f"Supported formats: {', '.join(constants.FORMAT.values())}")

    elif args.available_providers:
        # Show aditional help about models.
        print(f"Available Providers: {', '.join(constants.MODEL_PROVIDERS.values())}")

    else:
        pass


if __name__ == "__main__":
    main()
