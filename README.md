# Scrape & Chat: A Web Scraping and Chatbot Integration Application

## Problem Statement
The primary objective of this project is to create an application that combines web scraping and conversational AI capabilities. The application should allow users to scrape data from a given website and use this data to generate intelligent responses to user queries. This solves the problem of manually extracting website data and interpreting it for various use cases, saving time and effort for users.

## Approach
1. **Web Scraping:**
   - Use Selenium WebDriver to scrape websites, ensuring compatibility with dynamic web pages.
   - Extract essential information such as the page title, meta descriptions, keywords, headings, textual content, and links count.

2. **Conversational AI:**
   - Integrate with a conversational AI model (e.g., Llama or OpenAI’s GPT) to enable intelligent responses based on scraped data.
   - Structure responses to provide meaningful insights using the scraped data.

3. **GUI Integration:**
   - Build a user-friendly desktop application using PyQt5 for seamless interaction.
   - Include functionalities like URL input, scraping status updates, query input, and dynamic response display.

## Solution
The solution is a PyQt5-based GUI application that:

- Accepts a website URL for scraping.
- Extracts key information from the website using Selenium.
- Allows users to input questions about the scraped data.
- Uses a conversational AI API to provide intelligent answers based on the scraped data.

The application consists of the following components:

1. **Web Scraper:**
   - Implements headless Chrome for efficient data scraping.
   - Handles errors gracefully to ensure robustness.

2. **Conversational AI Integration:**
   - Utilizes an API endpoint for generating responses.
   - Customizes the chatbot's behavior based on the scraped data.

3. **Graphical User Interface (GUI):**
   - Provides an intuitive layout with two panels:
     - Left Panel: For inputting the website URL and initiating scraping.
     - Right Panel: For displaying the chat history and interacting with the chatbot.
   - Includes status updates, styled input fields, and buttons.

---

## Features

### Web Scraping
- Extracts:
  - Page title
  - Meta description
  - Meta keywords
  - Headings (H1 to H6)
  - Body text
  - Links count
- Ensures compatibility with dynamic web pages.
- Displays status updates during the scraping process.

### Chatbot
- Processes user questions based on scraped data.
- Customizes responses using structured system prompts.
- Utilizes a conversational AI model for intelligent and context-aware answers.

### GUI
- Clean and responsive design built with PyQt5.
- Split interface for scraping and chat functionalities.
- Real-time status updates and dynamic response display.

---

## Installation
### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Dependencies
Install the required Python packages using:
```bash
pip install -r requirements.txt
```
**Requirements file:**
```
PyQt5
selenium
webdriver-manager
requests
dotenv
```

---

## Usage
1. Clone the repository:
```bash
git clone https://github.com/singhrimiumesh/Scrape-Chat.git
cd scrape-chat
```

2. Create a `.env` file in the root directory with the following variables:
```
API_KEY=your_api_key
url=your_api_url
```

3. Run the application:
```bash
python app.py
```

4. In the GUI:
   - Enter a website URL in the input field and click "Scrape Website."
   - Once scraping is complete, ask questions about the scraped data in the chat interface.

---

## File Structure
```
scrape-chat/
├── Scrape_and_Chat.py   # Main application code
├── requirements.txt     # List of dependencies
├── .env                 # Example .env file for API configuration
├── README.md            # Documentation
└── LICENSE              # License information
```

---

## Example
1. **Scraping:**
   - Input: `https://example.com`
   - Output: Extracted website data (title, meta description, etc.).

2. **Chatbot Interaction:**
   - Input: "What is the main content of the website?"
   - Output: "The textual content of the website includes..."

---

## Challenges Faced
- Handling dynamic content and ensuring scraping compatibility.
- Creating an intuitive GUI for smooth user experience.
- Structuring system prompts to align chatbot responses with user expectations.

---

## Acknowledgments
- Thanks to PyQt5, Selenium, and OpenAI for making this project possible.

