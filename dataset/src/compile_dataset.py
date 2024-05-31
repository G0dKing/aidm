# compile_dataset.py

import pandas as pd

def compile_dataset(pdf_texts, transcripts, output_file):
    data = {
        'source': ['rulebook'] * len(pdf_texts) + ['transcript'] * len(transcripts),
        'text': pdf_texts + transcripts
    }

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(df.head())
