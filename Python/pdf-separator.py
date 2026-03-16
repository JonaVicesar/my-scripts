import PyPDF2
import os
import subprocess  # to open the file automatically after splitting
import sys

def get_colors():
    return {
        'C_RESET': '\033[0m',
        'C_VERDE': '\033[0;32m',
        'C_AZUL': '\033[0;34m',
        'C_CELESTE': '\033[0;36m',
        'C_ROJO': '\033[0;31m'
    }

c = get_colors()

def split_pdf(original_path, start_page, end_page, output_filename):
    try:
        with open(original_path, 'rb') as original_file:
            reader = PyPDF2.PdfReader(original_file)
            writer = PyPDF2.PdfWriter()

            for page_num in range(start_page, end_page + 1):
                page = reader.pages[page_num]
                writer.add_page(page)

            with open(output_filename, 'wb') as output_file:
                writer.write(output_file)
            return True
    except Exception as e:
        print(f"{c['C_RED']}\nAn error occurred: {e}{c['C_RESET']}")
        return False

def main():
    # keep asking until a valid pdf path is given
    while True:
        pdf_path = input(f"{c['C_CYAN']}Enter the PDF path: {c['C_RESET']}")
        if os.path.exists(pdf_path) and pdf_path.lower().endswith('.pdf'):
            break
        print(f"{c['C_ROJO']}Error: Invalid file.{c['C_RESET']}")

    try:
        with open(pdf_path, 'rb') as f:
            total_pages = len(PyPDF2.PdfReader(f).pages)
            print(f"{c['C_VERDE']}The PDF has {total_pages} pages.{c['C_RESET']}")
    except: return

    # validate range before continuing
    while True:
        try:
            start = int(input(f"Start page (1-{total_pages}): "))
            end = int(input(f"End page ({start}-{total_pages}): "))
            if 0 < start <= end <= total_pages:
                break
            print(f"{c['C_ROJO']}Invalid range.{c['C_RESET']}")
        except ValueError: pass

    # auto-generate output name if user leaves it blank
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    suggested = f"{base_name}_pages_{start}_to_{end}.pdf"
    output_name = input(f"Output name (Enter for '{suggested}'): ") or suggested
    if not output_name.lower().endswith('.pdf'): output_name += '.pdf'

    print(f"{c['C_AZUL']}Processing...{c['C_RESET']}")
    
    if split_pdf(pdf_path, start - 1, end - 1, output_name):  # -1 because PyPDF2 uses 0-based index
        full_path = os.path.abspath(output_name)
        print(f"{c['C_VERDE']}Success!{c['C_RESET']}")
        print(f"{c['C_CELESTE']}File saved at: {c['C_RESET']}{full_path}")
        
        open_file = input(f"\nDo you want to open the PDF now? (y/n): ").lower()
        if open_file == 'y':
            subprocess.run(['xdg-open', full_path])

if __name__ == "__main__":
    main()