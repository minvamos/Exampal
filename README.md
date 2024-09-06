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
     streamlit run streamlit_app.py
     ```
   - Access the application at `http://localhost:8501` in your web browser.

## Features

- **Input Exam Content**: Allows users to input exam content.
- **Generate Questions**: Generates questions based on the provided exam content.
- **Validate Answers**: Checks if the user-provided answers are correct.

## Example

1. **Input Exam Content**:

   - Enter exam content.
   - Example: "The capital of France is Paris."

2. **Generate Questions**:

   - Generates a question based on the exam content.
   - Example: "What is the capital of France?"

3. **Validate Answers**:
   - User inputs "Paris" as an answer.
   - The chatbot validates the answer and provides feedback.

## Note

This project is a prototype and may require further development and testing.
