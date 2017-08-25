

class DocConverter(object):
    """"""

    def load_file(self, file_name):
        """"""
        with open(file_name, 'r') as document_file:
            lines = document_file.readlines()
        return "".join(lines)

    def convert_pdf(self, file_content):
        """"""
        return file_content

    def convert(self, file_name):
        file_content = self.load_file(file_name)

        return self.convert_pdf(file_content)
