from kitties import ImageSearch
from config import DB_FILE, FAISS_INDEX_FILE

class VkBot:
    def __init__(self, user_id):
        self._USER_ID = user_id
        self.image_search = ImageSearch(DB_FILE, FAISS_INDEX_FILE)

    def new_message(self, text, attachments=None):
        image_url = None

        if "http" in text:
            image_url = text.strip()
            image_url = ''.join(image_url.split('amp;'))

        elif attachments:
            photo_sizes = attachments['photo']['sizes']
            max_res_photo = max(photo_sizes, key=lambda size: size['width'] * size['height'])
            image_url = max_res_photo['url']
            # не робит(

        if image_url:
            similar_images = self.image_search.search_similar_images(image_url=image_url)
            if similar_images:
                response = "Похожие картинки:\n" + "\n".join(similar_images)
                return response
            else:
                return "Ошиька(."

        else:
            return "Отправьте ссылку на картинку или фото для поиска похожих изображений."