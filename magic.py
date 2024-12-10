# import fitz  # PyMuPDF

# def print_pdf_characters(pdf_path):
#     # Open the PDF file
#     doc = fitz.open(pdf_path)

#     # Iterate through all pages in the document
#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)
        
#         # Extract text from the page
#         text = page.get_text("text")

#         # Print each character in the extracted text
#         for char in text:
#             print(char, end='')

#     doc.close()

# # Example usage
# pdf_path = 'input.pdf'  # Replace with your PDF file path
# print_pdf_characters(pdf_path)


import fitz  # PyMuPDF

def replace_words_in_pdf(pdf_path, output_pdf_path, old_word, new_word):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Iterate through all pages in the document
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extract the text from the page
        text = page.get_text("text")

        print(text)
        
        # Replace the old word with the new word
        # modified_text = text.replace(old_word, new_word)

        # Use the modified text to update the page
        # First, remove existing text
        # page.clean_contents()
        
        # Add the modified text (you may want to add additional formatting here if needed)
        # page.insert_text((0, 0), modified_text, fontsize=12)

    # Save the modified PDF
    doc.save(output_pdf_path)

    doc.close()

# Example usage
pdf_path = 'input.pdf'  # Path to your PDF
output_pdf_path = 'path_to_modified_pdf.pdf'  # Path to save modified PDF
old_word = 'Greetings'  # Word to be replaced
new_word = 'Beatings'  # Word to replace with

replace_words_in_pdf(pdf_path, output_pdf_path, old_word, new_word)
