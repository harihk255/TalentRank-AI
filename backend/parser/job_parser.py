from docx import Document


class JobParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def load_job_description(self):

        document = Document(self.file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs)