# Canada Innovation Chatbot

## Overview
To supplement the findings in this proposal, a chatbot was developed to provide responsive and accessible insights into Canada’s innovation strategy. The chatbot answers user inquiries based on four key areas:  
- **Information and Communication Technology**
- **High-Tech Manufacturing & Commercialization**
- **Clean Energy & Environmental Sustainability**
- **Creative Industries and Digital Content**

![chatbot logo](static/images/logoleaf.png)

---

## Setup Instructions

### Prerequisites
Ensure you have the following installed:  
- Python 3.x  
- `pip` (Python package manager)  
- `virtualenv` (optional but recommended)  
- Git  

### Installation

1. **Clone the repository**  
   ```sh
   git clone https://github.com/your-repo/innovation_chatbot.git
   cd innovation_chatbot

2. **Set API Key**
    ```python
    # line in app.py
    # replace with your DeepSeek API key
    API_KEY = "placehold"
    ```

2. **Set up a virtual environment (recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   .\venv\Scripts\activate  # On Windows

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt

4. **Run the chatbot server locally**
   ```sh
   python app.py

### Usage

- Open a web browser and go to http://127.0.0.1:5000/.
- Enter questions related to Canada’s innovation strategy.
- The chatbot will provide detailed and relevant responses based on curated knowledge.
- Follow-up questions are suggested to enhance understanding.
