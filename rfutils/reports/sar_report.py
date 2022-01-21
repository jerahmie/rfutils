"""
Generate a report for SAR calculations.
"""

from fpdf import FPDF


def create_sar_report():
    """create a pdf report of SAR comparisons
    """
    pdf = FPDF('P', 'in', 'Letter')
    print(dir(pdf))
    pdf.add_page()
    pdf.set_font('Times', 'B', 16)
    pdf.cell(3, 3, 'Hello World!', 1)
    pdf.ln(1)
    pdf.cell(3, 8, 'Powerered by FPDF.', 0, 1, 'C')
    pdf.output(name='test.pdf', dest='F')


if __name__ == "__main__":
    print("Generating SAR report")
    create_sar_report()
