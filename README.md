# Exampal 

![Eng video to GIF](https://github.com/user-attachments/assets/14ac1081-9e9c-4b93-9abb-1972d3d37d05)

**ExamPal** is a chatbot project designed to generate 8 exam questions based on user-provided content. The name "ExamPal" incorporates a clever wordplay: "Pal" refers to the Korean pronunciation of the number 8 (팔, "pal"), while also meaning "friend" in English. Thus, ExamPal symbolizes a friend that helps you generate 8 exam questions.
## Usage

1. **Setup**:

   - Navigate to the project directory.
   - Install the required packages listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

2. **API Token Configuration**:

   - Set your Hugging Face API token in the `config/settings.py` file. The file should look like this:

     ```python
     import os

     HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
     ```

   - Make sure the API token is set as the environment variable `HUGGINGFACE_API_TOKEN`.

3. **Run Streamlit Application**:
   - Start the Streamlit application with the following command:
     ```bash
     streamlit run main.py
     ```
   - Access the application at `http://localhost:8501` in your web browser.

## Features

- **Input Exam Content**: Users can input exam content in the designated section.
- **Generate Questions**: The application generates 8 questions based on the provided exam content.

## Example

1. **Input Exam Content**:

   - Enter exam content in the provided text area.
   - Example: "The capital of France is Paris."

2. **Generate Questions**:

   - After entering the exam content, 8 questions will be generated and displayed in the "Questions:" section shortly after.

## Note

This project is a prototype and may require further development and testing.

Future development plans include adding answer verification logic and additional question generation logic.
