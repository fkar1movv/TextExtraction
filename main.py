import fitz 
import json
import re

def extract_text_by_section(pdf_path, output):
    doc = fitz.open(pdf_path)
    extracted_data = {}
    
    # Pattern to recognize all-caps headings
    heading_pattern = re.compile(r'^[А-ЯЁ\s]+$')
    
    # Reading through page by page
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        page_text = page.get_text("text")
        
        page_data = {
            "title": f"Page {page_num + 1}",
            "sections": {}
        }
        
        # Split text into paragraphs based on two or more newlines
        paragraphs = re.split(r'\n\s*\n', page_text.strip())
        
        section_counter = 1 
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            
            # If the paragraph is all-caps (heading), treat it as a standalone section
            if heading_pattern.match(paragraph):
                section_data = {
                    "title": paragraph,
                    "subsections": {}
                }
                page_data["sections"][str(section_counter)] = section_data
                section_counter += 1
                continue
            
            # Split by sentences but avoid breaking on abbreviations like "т. д."
            sentences = re.split(r'(?<!т)\.\s+', paragraph)
            
            section_data = {
                "title": f"Section {section_counter}",
                "subsections": {}
            }
            
            # If paragraph contains multiple sentences, treat them as subsections
            if len(sentences) > 1:  
                for subsection_num, sentence in enumerate(sentences, start=1):
                    section_data["subsections"][f"{section_counter}.{subsection_num}"] = {
                        "title": f"Subsection {section_counter}.{subsection_num}",
                        "text": sentence.strip()
                    }
            else:
                # If the paragraph is short and doesn't need subsections, just treat it as a section
                section_data["text"] = paragraph.strip()

            # Add section to page data
            page_data["sections"][str(section_counter)] = section_data
            section_counter += 1
        
        # Add page data to the final extracted data
        extracted_data[str(page_num + 1)] = page_data
    
    # Save the extracted structure to JSON
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)



document = "Руководство_Бухгалтерия_для_Узбекистана_ред_3_0.pdf"
output = "structure.json"
extract_text_by_section(document, output)
