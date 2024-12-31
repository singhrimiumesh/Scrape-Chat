from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")
url = os.getenv("url")


from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QTextBrowser, QMessageBox, QSplitter
)
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

# Scraping function
def scrape_website(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    extracted_data = {}

    try:
        driver.get(url)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        extracted_data["title"] = driver.title

        try:
            extracted_data["meta_description"] = driver.find_element(
                By.XPATH, "//meta[@property='og:description']"
            ).get_attribute("content")
        except Exception:
            extracted_data["meta_description"] = "No meta description found."

        try:
            extracted_data["meta_keywords"] = driver.find_element(
                By.XPATH, "//meta[@name='keywords']"
            ).get_attribute("content")
        except Exception:
            extracted_data["meta_keywords"] = "No meta keywords found."

        headings = {}
        for level in range(1, 7):
            heading_tag = f"h{level}"
            headings[heading_tag] = [
                h.text for h in driver.find_elements(By.TAG_NAME, heading_tag) if h.text
            ]
        extracted_data["headings"] = headings

        extracted_data["textual_data"] = driver.find_element(By.TAG_NAME, "body").text
        extracted_data["links_count"] = len(driver.find_elements(By.TAG_NAME, "a"))

    except Exception as e:
        extracted_data["error"] = str(e)
    finally:
        driver.quit()

    return extracted_data

# API call function
def get_response(prompt, scraped_data):
    system_prompt = (
        f"You are an intelligent assistant bot. Data includes:\n"
        f"Title: {scraped_data.get('title', 'No title')}\n"
        f"Meta Description: {scraped_data.get('meta_description', 'No meta description')}\n"
        f"Headings: {scraped_data.get('headings', 'No headings')}\n"
        f"Links Count: {scraped_data.get('links_count', 'No links')}\n"
        f"Textual Content: {scraped_data.get('textual_data', 'No text')}\n\n"
        "Answer the user's question based only on this data."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    data = {
        "messages": messages,
        "model": "llama3-8b-8192",
        "temperature": 0.7
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"API Error: {e}"

# GUI Application
class ChatBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.scraped_data = {}

    def init_ui(self):
        self.setWindowTitle("Scrape & Chat")
        self.setGeometry(100, 100, 900, 600)

        # Layouts
        main_layout = QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        # Left Panel (Scraping)
        self.url_label = QLabel("Enter Website URL:")
        self.url_input = QLineEdit()
        self.scrape_button = QPushButton("Scrape Website")
        self.scrape_button.clicked.connect(self.scrape_website)
        self.status_label = QLabel("Status: Waiting for input...")

        self.url_input.setStyleSheet("padding: 8px; border-radius: 8px; border: 1px solid #ccc;")
        self.scrape_button.setStyleSheet(
            "padding: 10px; border-radius: 8px; background-color: #4CAF50; color: white; font-weight: bold;"
        )
        self.status_label.setStyleSheet("color: #555; font-style: italic;")

        left_panel.addWidget(self.url_label)
        left_panel.addWidget(self.url_input)
        left_panel.addWidget(self.scrape_button)
        left_panel.addWidget(self.status_label)

        # Right Panel (Chat)
        self.chat_area = QTextBrowser()
        self.chat_area.setStyleSheet(
            "background-color: #f9f9f9; padding: 10px; border-radius: 8px;"
        )
        self.chat_area.setFont(QFont("Arial", 10))

        self.prompt_label = QLabel("Ask a Question:")
        self.prompt_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        self.prompt_input.setStyleSheet("padding: 8px; border-radius: 8px; border: 1px solid #ccc;")
        self.send_button.setStyleSheet(
            "padding: 10px; border-radius: 8px; background-color: #007BFF; color: white; font-weight: bold;"
        )

        right_panel.addWidget(self.chat_area)
        right_panel.addWidget(self.prompt_label)
        right_panel.addWidget(self.prompt_input)
        right_panel.addWidget(self.send_button)

        # Add panels to splitter
        left_widget = QWidget()
        right_widget = QWidget()
        left_widget.setLayout(left_panel)
        right_widget.setLayout(right_panel)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        # Add splitter to main layout
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def scrape_website(self):
        url = self.url_input.text().strip()
        if not urlparse(url).scheme in ["http", "https"]:
            QMessageBox.critical(self, "Error", "Invalid URL")
            return

        self.status_label.setText("Status: Scraping website...")
        self.scraped_data = scrape_website(url)
        self.status_label.setText("Status: Scraping completed✅")

    from PyQt5.QtCore import QTimer

    def send_message(self):
        prompt = self.prompt_input.text().strip()
        if not prompt:
            return

        # User message in light green background
        user_message = f"""
        <div style="margin: 5px; padding: 10px; border-radius: 10px; color: #000">
            <span style = "background-color: #d1f7c4;"><b>You: </b>{prompt} </span>
        </div>
        """
        self.chat_area.append(user_message)

        # Disable the input and button while waiting
        self.prompt_input.setDisabled(True)
        self.send_button.setDisabled(True)

        # Function to show the bot's response after 1 second
        def display_bot_response():
            response = get_response(prompt, self.scraped_data)

            bot_message = f"""
            <div style="background-color: #CBC3E3; margin: 5px; padding: 10px; border-radius: 10px; color: #000; border: 1px solid #000;">
                <b>Bot: </b> {response}
            </div>
            """
            self.chat_area.append(bot_message)
            self.prompt_input.clear()

            # Re-enable the input and button
            self.prompt_input.setDisabled(False)
            self.send_button.setDisabled(False)

        # Set a 1-second delay for the bot's response
        QTimer.singleShot(500, display_bot_response)


# Main
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    chatbot_app = ChatBotApp()
    chatbot_app.show()
    sys.exit(app.exec_())
