import os
import pandas as pd
from fpdf import FPDF
from manageyourdata import metrics
import pdf_generator as pdf_generator
from utils import constants


class DataManager:

    data: pd.DataFrame = None
    file_name: str = None   

    def load_data(self, file_path: str) -> pd.DataFrame:
        """General function to read data provided by the user.

        Args:
            file_path (str): Route to the data file.

        Raises:
            ValueError: File format not supported.
        """    

        self.file_name = os.path.basename(file_path)

        if file_path.endswith(".csv"):
            self.data = pd.read_csv(file_path)
        
        elif file_path.endswith(".xlsx"):
            self.data = pd.read_excel(file_path)

        else:
            raise ValueError("File format not supported. Use --sf to show all available options.")
        
    
    def report_pdf(self, output_path: str):
        """Generate the default PDF report template.

        Args:
            output_path (str): Destination to save the report.
        """                

        details = metrics.obtain_details(self.data, self.file_name)
        columns = metrics.obtain_columns(self.data)

        pdf = FPDF()
        pdf.add_page()
        pdf_generator.heading(pdf)
        pdf_generator.general_info(pdf, details)
        pdf_generator.columns_info(pdf, columns)
        pdf.output(output_path, 'F')


    def export_data(self, option: str) -> None:
        """General function to export in determined format.

        Args:
            option (str): Desired way to export the data.

        Raises:
            ValueError: Export format not supported.
        """        

        file_extension = constants.FORMAT[option]
        export_path = f"exports/{self.file_name}-exported{file_extension}"
        
        if file_extension == ".csv":
            self.data.to_csv(export_path, index=False)

        elif file_extension == ".xlsx":
            self.data.to_excel(export_path, index=False)

        else:
            raise ValueError("Export format not supported.")
