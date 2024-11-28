from py_pdf_parser.loaders import load_file
from pathlib import Path
import os
import pandas as pd
import json
import spacy
from spacy.tokens import DocBin, Doc
import numpy as np
from multiprocessing import Pool
import pickle

BASE_DIR = Path(__file__).parent
os.chdir(BASE_DIR)

save_path = "./docs_new"
nlp = spacy.load("de_dep_news_trf")

def extract_text(path):

    document = load_file(path)
    pages = document.page_numbers
    elements = document.elements.filter_by_pages(pages[1:])
    text = " ".join([i.text() for i in elements if len(i.text()) > 100])
    return text


dummy= r"C:\Users\miche\Documents\Data Science - Alfatraining\Data Analyst\fragdenstaat\data\data\docs.json"
 
df = pd.json_normalize(json.loads(Path(dummy).read_text())["json_docs"])
df.drop(["pages", 'public', 'listed', 'allow_annotation',
'pending', 'cover_image', 'page_template',
'outline', 'uid', 'pages_uri', 'original', 'foirequest', 'publicbody',
'properties._tables', 'properties.creator', 'properties._format_webp'], 
        inplace=True, axis=1)

df["file_name"] = df["file_url"].apply(lambda x: x.rsplit("/", 1)[1])
df = df[df["data.year"] >= 2019]
df = df[df["data.year"] <= 2022]
# df = df[df["data.issue"] <= 12]
with open(save_path + "/"+ "df.pickle","wb") as f:
    df.to_pickle(f)

def spacy_it(path):
    import spacy
    nlp = spacy.load("de_dep_news_trf")
    return nlp(extract_text(path))
folder = r"C:\Users\miche\Documents\Data Science - Alfatraining\Data Analyst\fragdenstaat\data\docs_pdf"
paths = [Path(folder+r"\\"+file) for file in df["file_name"].values]

# to_pool = [map(spacy_it, paths)]
    
if __name__ == '__main__':
    with Pool(5) as p:
    #     all_docs = p.map(spacy_it, np.array_split(paths, 20))

    # doc_bin = DocBin(store_user_data=True, docs=all_docs)
    # doc_bin.to_disk( save_path + "/data.spacy")
        all_txt = p.map(extract_text, np.array_split(paths, 20) )
    pickle.dump(all_txt,open( save_path + "/raw_txt.pickle", "wb"))