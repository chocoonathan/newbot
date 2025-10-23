import os

import aiohttp
import requests

from config import API_MAELYN, COOKIES_U_BING


class Bing:
    def __init__(self):
        self.api_key = API_MAELYN
        self.cookie = COOKIES_U_BING
        self.base_url = "https://api.maelyn.sbs/api/bing/createimage"

    async def generate_images(
        self,
        folder_name: str,
        prompt: str,
    ):
        """Generate images using Maelyn API"""
        try:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            params = {
                "cookie": self.cookie,
                "prompt": prompt,
                "aspectRatio": "1:1",
            }

            headers = {"mg-apikey": self.api_key}

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.base_url, headers=headers, params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()

                        if data.get("status") == "Success" and data.get("code") == 200:
                            image_urls = data.get("result", [])

                            if not image_urls:
                                return folder_name, []

                            downloaded_images = []
                            for i, img_url in enumerate(image_urls):
                                try:
                                    async with session.get(img_url) as img_response:
                                        if img_response.status == 200:
                                            img_data = await img_response.read()
                                            img_path = os.path.join(
                                                folder_name, f"bing_{i+1}.jpg"
                                            )

                                            with open(img_path, "wb") as f:
                                                f.write(img_data)

                                            downloaded_images.append(img_path)
                                except Exception as e:
                                    print(f"Error downloading image {i+1}: {e}")
                                    continue

                            return folder_name, downloaded_images
                        else:
                            error_msg = data.get("message", "Unknown API error")
                            raise Exception(f"API Error: {error_msg}")
                    else:
                        raise Exception(f"HTTP Error: {response.status}")

        except Exception as e:
            raise Exception(f"Generate images failed: {str(e)}")

    def generate_images_sync(
        self, folder_name: str, prompt: str, aspect_ratio: str = "1:1"
    ):
        """Sync version for backup"""
        try:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            params = {
                "cookie": self.cookie,
                "prompt": prompt,
                "aspectRatio": aspect_ratio,
            }

            headers = {"mg-apikey": self.api_key}

            response = requests.get(self.base_url, headers=headers, params=params)
            data = response.json()

            if data.get("status") == "Success" and data.get("code") == 200:
                image_urls = data.get("result", [])
                downloaded_images = []

                for i, img_url in enumerate(image_urls):
                    try:
                        img_response = requests.get(img_url)
                        if img_response.status_code == 200:
                            img_path = os.path.join(folder_name, f"bing_{i+1}.jpg")
                            with open(img_path, "wb") as f:
                                f.write(img_response.content)
                            downloaded_images.append(img_path)
                    except Exception as e:
                        print(f"Error downloading image {i+1}: {e}")
                        continue

                return folder_name, downloaded_images
            else:
                error_msg = data.get("message", "Unknown API error")
                raise Exception(f"API Error: {error_msg}")

        except Exception as e:
            raise Exception(f"Generate images failed: {str(e)}")
