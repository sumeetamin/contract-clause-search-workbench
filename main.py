"""Local TF-IDF clause search that returns source IDs and text spans."""
import argparse
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",required=True);p.add_argument("--query",required=True);p.add_argument("--id",default="clause_id");p.add_argument("--text",default="text");p.add_argument("--top-k",type=int,default=10);p.add_argument("--out",default="outputs");a=p.parse_args()
 d=pd.read_csv(a.input).dropna(subset=[a.text]).reset_index(drop=True)
 if d.empty:raise SystemExit("No clause text found.")
 vectorizer=TfidfVectorizer(ngram_range=(1,2),min_df=1,sublinear_tf=True,stop_words="english");matrix=vectorizer.fit_transform(d[a.text].astype(str));q=vectorizer.transform([a.query]);scores=cosine_similarity(q,matrix).ravel();idx=scores.argsort()[::-1][:a.top_k]
 idcol=d[a.id] if a.id in d else pd.Series(d.index.astype(str))
 results=pd.DataFrame({"source_id":idcol.iloc[idx].astype(str),"similarity":scores[idx],"clause_text":d[a.text].iloc[idx].astype(str)})
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True);results.to_csv(out/"search_results.csv",index=False);print(results.to_string(index=False))
if __name__=="__main__":main()
