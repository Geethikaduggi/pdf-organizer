import os
import re
import shutil
import pdfplumber
from datetime import datetime

# 📁 Define input and output folders
INPUT_FOLDER = "sample_pdfs"
OUTPUT_FOLDER = "organized_pdfs"

# 🔧 Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_info(pdf_path):
    """
    Extracts title and date from the first page of a PDF file.
    """
    try:
        # Open the PDF
        with pdfplumber.open(pdf_path) as pdf:
            # Get text from the first page
            first_page = pdf.pages[0]
            text = first_page.extract_text() or ""
    except Exception as e:
        print(f"❌ Could not read {pdf_path}: {e}")
        return datetime.today().strftime("%Y_%m_%d"), "untitled"

    # ✏️ Get the first line of text as the title
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        raw_title = lines[0]
        # Take first 5–7 words and clean up symbols
        title = "_".join(raw_title.split()[:7])
        title = re.sub(r"[^\w_]", "", title).lower()
    else:
        title = "untitled"

    # 🗓️ Try to extract a date from the text (any page)
    date_match = re.search(r"(\d{4}[-/]\d{2}[-/]\d{2})|(\d{2}[-/]\d{2}[-/]\d{4})", text)
    if date_match:
        raw_date = date_match.group()
        try:
            # Try to parse the date (multiple formats)
            if "-" in raw_date:
                date = datetime.strptime(raw_date, "%Y-%m-%d")
            else:
                date = datetime.strptime(raw_date, "%d/%m/%Y")
        except:
            date = datetime.today()
    else:
        date = datetime.today()

    date_str = date.strftime("%Y_%m_%d")
    return date_str, title

def organize_pdfs():
    """
    Goes through each PDF, extracts its title and date,
    renames the file, and moves it into a date-named folder.
    """
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(INPUT_FOLDER, filename)
            date_str, title = extract_info(input_path)

            # 🔒 Make a folder for the date
            folder_path = os.path.join(OUTPUT_FOLDER, date_str)
            os.makedirs(folder_path, exist_ok=True)

            # 📄 New filename: title + date
            new_filename = f"{title}_{date_str}.pdf"
            destination_path = os.path.join(folder_path, new_filename)

            # 📥 Copy the PDF into the new location
            shutil.copy(input_path, destination_path)
            print(f"✅ Moved: {filename} → {folder_path}/{new_filename}")

# ▶️ Main function
if __name__ == "__main__":
    organize_pdfs()
