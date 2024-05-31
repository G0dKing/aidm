# main.py

import os
from dotenv import load_dotenv
from drive_access import download_files_from_drive
from pdf_extraction import extract_text_from_pdfs
from youtube_transcripts import get_youtube_transcripts, get_video_ids_from_playlist
from text_cleaning import clean_text, segment_sentences
from compile_dataset import compile_dataset

load_dotenv()

def main():
    # Extract Text Data from Google Drive Folder
    drive_folder_id = os.getenv('DRIVE_FOLDER_ID')
    extracted_texts = extract_files_from_drive(drive_folder_id)
    pdf_texts = extract_text_from_pdfs(output_dir)

    # Extract Transcripts from YT Playlists
    youtube_playlist_ids = ['YT_PLAYLIST_ID_1', 'YT_PLAYLIST_ID_2', 'YT_PLAYLIST_ID_3', 'YT_PLAYLIST_ID_4', 'YT_PLAYLIST_ID_5', 'YT_PLAYLIST_ID_6']
    youtube_video_ids = get_video_ids_from_playlist(playlist_id)
    youtube_transcripts = get_youtube_transcripts(youtube_video_ids)

    # Step 4: Prepare Text for AI
    cleaned_texts = [clean_text(text) for text in extracted_texts]
    cleaned_transcripts = [clean_text(transcript) for transcript in youtube_transcripts]

    segmented_texts = [segment_sentences(text) for text in cleaned_texts]
    segmented_transcripts = [segment_sentences(transcript) for transcript in cleaned_transcripts]

    flat_texts = [sentence for sublist in segmented_texts for sentence in sublist]
    flat_transcripts = [sentence for sublist in segmented_transcripts for sentence in sublist]

    # Step 5: Compile Dataset
    output_csv = os.getenv('OUTPUT_CSV')
    compile_dataset(flat_texts, flat_transcripts, output_csv)

if __name__ == '__main__':
    main()
