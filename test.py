import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
import requests

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = input("Provide your Google API key here: ")

class Document:
    def __init__(self, page_content):
        self.page_content = page_content


def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join(entry['text'] for entry in transcript)

        with open('temp.txt', 'w', encoding='utf-8') as file:
            file.write(transcript_text)

        return transcript_text.strip()
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return "Transcript not found"
    
def embed_and_query_chroma(query):
     
    loader = TextLoader("temp.txt")
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    db = Chroma.from_documents(docs, embedding_function)

    query = query
    docs = db.similarity_search(query)

    return docs[0].page_content if docs else "No relevant information found"




def generate_response(user_message, transcript):
    response = requests.post(
        "https://api.naga.ac/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer ng-z0E45NH0iumvObnSpUt5BAeboEWw1",
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": transcript},
            ],
            "temperature": 0.7,
        },
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"Error {response.status_code}: {response.text}"

if __name__ == "__main__":
    youtube_url = input("Enter a YouTube URL: ")
    video_id = youtube_url.split('v=')[-1]
    full_transcript = get_youtube_transcript(video_id)

    print(f"YouTube Transcript:\n{full_transcript}")

    while True:
        user_message = input("You: ")
        if user_message.lower() == "exit":
            break
        relevant_part = embed_and_query_chroma(user_message)
        print(f"Relevant part:\n{relevant_part}\n")
        response = generate_response(user_message, relevant_part)
        print(f"AI: {response}\n")