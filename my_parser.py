# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:45:22 2024

@author: miche
"""

from py_pdf_parser.loaders import load_file
from py_pdf_parser.visualise import visualise
import os
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent.parent
os.chdir(BASE_DIR)

"""
Diese Datei wurde benutzt um bestimmte Bilder für die Powerpoint Präsentation zu generieren.
Sie ist in diesem github, da andere Dateien funktionen aus dieser Datei importieren.
"""



def ordering_function(elements):
    """
    Note: Elements will be PDFMiner.six elements. The x axis is positive as you go left
    to right, and the y axis is positive as you go bottom to top, and hence we can
    simply sort according to this.
    """
    print("elements")
    return sorted(elements, key=lambda elem: (elem.x0, elem.y0))  

def parser(pdf_path, page_number, **kwargs):
    """
    This function also removes text elements with less han 101 Tokens, as part of the
    datacleaning. e.g. removing descriptions of images and diagramms, too short to learn 
    something from it.
    """
    document = load_file(pdf_path)
    elements = document.elements.filter_by_page(page_number)
    text_list = [i.text() for i in elements if len(i.text()) > 100]
    return " ".join(text_list)
    
if __name__ == '__main__':
    dummy = r"C:\Users\miche\Documents\Data Science - Alfatraining\Data Analyst\fragdenstaat\daten-grab\gmbl-nr-43-2023.pdf"
    # hier zwischen default ordering left to right, top to bottoom
    document = load_file(dummy)#, element_ordering=ordering_function)
    pages = document.page_numbers
    elements = document.elements.filter_by_pages(pages[1:])
    text = " ".join([i.text() for i in elements if len(i.text()) > 100])
    
    test = document.elements
    
    ele_list_font = [[i.text(), i.page_number, i.font_size, 
                      i.bounding_box.x0, i.bounding_box.y0, 
                      i.bounding_box.x1, i.bounding_box.y1, len(i.text())] 
                     for i in test]
    col_list = ["text", "page", "font_size", "x0", "y0", "x1", "y1", "len"]
    
    df = pd.DataFrame(ele_list_font, columns=col_list)
    
    
    
    # macht ein Fenster auf (bzw. 2), wenn pip install py-pdf-parser[dev]
    visualise(document, show_info=True)
    
    document.elements.filter_by_page(2)
