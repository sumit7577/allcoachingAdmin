import csv
import docx
from django.core.files.base import File

class TestSeriesExtractor:
    def __init__(self, file: File, name: str):
        self.file = file
        self.name = name

    def is_csv(self) -> bool:
        """Check if the file is a valid CSV"""
        if not self.file.name.lower().endswith(".csv"):
            return False
        try:
            self.file.seek(0)
            csv.Sniffer().sniff(self.file.read(1024).decode("utf-8",errors="ignore"))
            self.file.seek(0)
            return True
        except Exception as e:
            print(e)
            return False

    def is_docx(self) -> bool:
        """Check if the file is a valid DOCX"""
        if not self.file.name.lower().endswith(".docx"):
            return False
        try:
            self.file.seek(0)  # Ensure reading from start
            docx.Document(self.file)
            return True
        except Exception:
            return False

    def extract_questions(self):
        """Extract questions based on file type"""
        if self.is_csv():
            return self.extract_from_csv()
        elif self.is_docx():
            return self.extract_from_docx()
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or DOCX file.")

    def extract_from_csv(self):
        """Extract questions from a CSV file"""
        self.file.seek(0)  # Ensure reading from the start
        reader = csv.reader(self.file.read().decode("utf-8",errors="ignore").splitlines())
    
        headers = next(reader, None)  # Extract headers
        if not headers:
            return [], []  # Return empty lists if no headers exist

        structured_data = []
        solution_data = []

        for row in reader:
            if len(row) >= len(headers):
                question_data = {headers[i]: row[i] for i in range(len(headers))}

                # Process options
                options = [question_data.get(f"option{chr(65+i)}", "") for i in range(4)]
                options = [opt for opt in options if opt]  # Remove empty options

                structured_entry = {
                    "Question": question_data.get("question", ""),
                    "Option": options,
                    "Type": question_data.get("type", ""),
                    "Negative Marks": question_data.get("negative_marks", ""),
                    "Positive Marks": question_data.get("positive_marks", "")
                }

                # Process correct option and explanation separately
                answer_solution = {
                    "Answer": question_data.get("correctOpt", ""),
                    "Solution": question_data.get("explanation", ""),
                    "Question": question_data.get("question", "")
                }

                structured_data.append(structured_entry)
                solution_data.append(answer_solution)
                    
        return structured_data, solution_data
    

    def extract_from_docx(self):
        """Extract questions from a DOCX file"""
        if not self.file:
            return [], []

        try:
            document = docx.Document(self.file)
        except Exception as e:
            print(f"Error reading document: {e}")
            return [], []

        table_data = []
        answer_solution_data = []

        for table in document.tables:
            table_dict = {}
            answer_solution = {}

            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                if len(cells) >= 2:
                    key, value = cells[0], cells[1]

                    # Store "Answer" and "Solution" separately
                    if key in ["Answer", "Solution"]:
                        answer_solution[key] = value
                    else:
                        if key in table_dict:
                            if isinstance(table_dict[key], list):
                                table_dict[key].append(value)
                            else:
                                table_dict[key] = [table_dict[key], value]
                        else:
                            table_dict[key] = value

                    if key == "Question":
                        answer_solution[key] = value

            if table_dict:
                table_data.append(table_dict)
            if answer_solution:
                answer_solution_data.append(answer_solution)

        return table_data, answer_solution_data
