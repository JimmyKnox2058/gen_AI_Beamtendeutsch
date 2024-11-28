# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 12:11:13 2024


Diese Datei liest die PDFs aus von 2023, inklusive datacleaning und tokenizing.
Sie ist zur vollständigkeit 2 mal da, um Rechenzeit zu sparen wurden die bereits generieten
Daten gemerged mit denen von 2022.
"""
import pandas as pd
import pickle
import json
from spacy.tokens import DocBin, Doc
import numpy as np
import spacy
from spacy.vocab import Vocab
import spacypdfreader
import pytesseract
from spacypdfreader import pdf_reader

from pathlib import Path
import os
import my_parser as my_p
#    return str(pytesseract.image_to_string(img, **kwargs)).replace("-\n\n", "").replace("-\n", "")

BASE_DIR = Path(__file__).parent
os.chdir(BASE_DIR)

dummy= r"C:\Users\miche\Documents\Data Science - Alfatraining\Data Analyst\fragdenstaat\data\data\docs.json"
 
df = pd.json_normalize(json.loads(Path(dummy).read_text())["json_docs"])
df.drop(["pages", 'public', 'listed', 'allow_annotation',
'pending', 'cover_image', 'page_template',
'outline', 'uid', 'pages_uri', 'original', 'foirequest', 'publicbody',
'properties._tables', 'properties.creator', 'properties._format_webp'], 
        inplace=True, axis=1)

df["file_name"] = df["file_url"].apply(lambda x: x.rsplit("/", 1)[1])
df = df[df["data.year"] == 2022]
# df = df[df["data.year"] <= 2019]
# df = df[df["data.issue"] <= 12]
with open("df.pickle","wb") as f:
    df.to_pickle(f)
    
def map_load(doc_path="./doc_trf_3", split=False)-> map:
    """
     Dieses script sucht alle Dateien im Verzeichnes des Scripts.
     Dann wird das ganze mit der load Funktion gemapt, dadurch entsteht ein 
     iterable dieser wird returned
    """
    files_list = [pos_file for pos_file in os.listdir(doc_path) if pos_file.endswith("spadoc")]
    def load_da_doc(filename):
        result = Doc(Vocab(lang="de")).from_disk(Path(doc_path+"/"+filename))
        if split:
            result._.pdf_file_name = result._.pdf_file_name.rsplit("\\", 1)[1]
        return result
    # test = itertools.chain.from_iterable(map(load_da_json, dummy))
    return map(load_da_doc, files_list)

folder = r"C:\Users\miche\Documents\Data Science - Alfatraining\Data Analyst\fragdenstaat\data\docs_pdf"
paths = [folder + "\\" + i for i in df.file_name]
#nlp = spacy.load("de_core_news_lg")
nlp = spacy.load("de_dep_news_trf")

if __name__ == '__main__':
    
    for pages, file in df[["num_pages", "file_name"]].values:
        doc = pdf_reader(folder+"\\"+file, nlp, my_p.parser, n_processes=20, lang="deu", page_range=(2, pages-1))
        # vergessen beim ersten durchlauf, falls erneuter duchlauf
        # ähnliche Zeile bei merger .py raus nehmen
        doc._.pdf_file_name = doc._.pdf_file_name.rsplit("\\", 1)[1]
        doc.to_disk("./doc_trf_3/" + file.split(".")[0] + ".spadoc")
        #doc_bin.add(doc)
    
    # TODO irgendwas is hier verbugt, warning prüfen
    doc_bin = DocBin(store_user_data=True, docs=map_load())
    doc_bin.to_disk("./doc_trf_3/data.spacy")
    

    

