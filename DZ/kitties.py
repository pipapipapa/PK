import torch
import clip
from PIL import Image
import json
import os
import faiss
import numpy as np
import requests
from io import BytesIO
from config import DB_FILE, FAISS_INDEX_FILE


class ImageSearch:
    def __init__(self, db_file=DB_FILE, faiss_index_file=FAISS_INDEX_FILE):
        self.db_file = db_file
        self.faiss_index_file = faiss_index_file
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.db = self.load_db()

        if os.path.exists(self.faiss_index_file):
            self.faiss_index = faiss.read_index(self.faiss_index_file)
            self.image_urls = list(self.db.keys())

        else:
            self.faiss_index, self.image_urls = self.build_faiss_index()

    def load_db(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return {}

    def save_db(self):
        with open(self.db_file, "w") as f:
            json.dump(self.db, f)

    def download_image(self, image_url):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            return image
        except Exception as e:
            print(e)
            return None

    def get_image(self, image_url):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def get_image_embedding(self, image_url):
        image = self.download_image(image_url)
        if image:
            try:
                image = self.preprocess(image).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    return self.model.encode_image(image).cpu().numpy().astype('float32')
            except Exception as e:
                print(f"Error processing image: {e}")
        return None

    def add_to_db(self, image_url):
        if image_url in self.db:
            print(f"{image_url} уже есть.")
            return False
        embedding = self.get_image_embedding(image_url)
        if embedding is not None:
            self.db[image_url] = embedding.tolist()
            self.save_db()
            self.faiss_index, self.image_urls = self.build_faiss_index()  # Rebuild index
            print(f"Added {image_url}")
            return True
        else:
            print(f"Ошибка добавления")
            return False

    def build_faiss_index(self):
        embeddings = []
        image_urls = []
        for url, embedding_list in self.db.items():
            embeddings.append(np.array(embedding_list))
            image_urls.append(url)

        if not embeddings:
            print("KYS")
            return None, []

        embeddings = np.array(embeddings).astype('float32')
        embeddings = embeddings.reshape(len(embeddings), -1)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        faiss.write_index(index, self.faiss_index_file)
        return index, image_urls

    def search_similar_images(self, image_url, n=5, similarity_threshold=-10e10):
        query_embedding = self.get_image_embedding(image_url)
        if query_embedding is None:
            return []

        D, I = self.faiss_index.search(query_embedding, n)

        similar_image_urls = []
        for i, distance in zip(I[0], D[0]):
            similarity = 1 - distance / np.sqrt(2)
            if similarity >= similarity_threshold:
                similar_image_urls.append(self.image_urls[i])
        return similar_image_urls

    def search_by_text(self, text, n=5, similarity_threshold=-10e10):  # Проверяет на наличие текста в итоге
        with torch.no_grad():
            text_input = clip.tokenize([text]).to(self.device)
            query_embedding = self.model.encode_text(text_input).cpu().numpy().astype('float32')
        if query_embedding is None:
            return []

        D, I = self.faiss_index.search(query_embedding, n)

        similar_image_urls = []
        for i, distance in zip(I[0], D[0]):
            similarity = 1 - distance / np.sqrt(2)
            if similarity >= similarity_threshold:
                similar_image_urls.append(self.image_urls[i])
        return similar_image_urls
