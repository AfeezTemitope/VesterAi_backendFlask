import unittest
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from parsers.pdf_parser import parse_pdf


def create_sample_pdf(path):
    """Generate a PDF file with content"""
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, "Sample PDF content for test")
    c.drawString(100, 735, "Slide 1")
    c.drawString(100, 720, "More sample content here.")
    c.save()


def create_wrong_pdf(path):
    """create a file with a wrong format that isn`t a proper PDF"""
    with open(path, 'w') as f:
        f.write("this is not a valid PDF file")


class TestPDFParser(unittest.TestCase):
    def setUp(self):
        """Create a valid sample PDF file for testing"""
        self.sample_pdf_path = 'tests/sample.pdf'
        create_sample_pdf(self.sample_pdf_path)

        # invalid pdf format
        self.invalid_pdf_format = 'tests/invalid.pdf'
        create_wrong_pdf(self.invalid_pdf_format)

    def test_valid_pdf(self):
        """This part will call your PDF parser"""
        slides = parse_pdf(self.sample_pdf_path)

        self.assertGreater(len(slides), 0, "Expected at least one slide")
        self.assertEqual(slides[0]['title'], 'Slide 1')
        self.assertIn("Sample PDF content for test", slides[0]['content'])

    def test_invalid_pdf(self):
        """Test parsing an invalid PDF file"""
        with self.assertRaises(Exception) as context:
            parse_pdf(self.invalid_pdf_format)
        self.assertIn("EOF marker not found", str(context.exception))

    def tearDown(self):
        """ Clean up the sample PDF generated. """
        os.remove(self.sample_pdf_path)
        if os.path.exists(self.invalid_pdf_format):
            os.remove(self.invalid_pdf_format)


if __name__ == '__main__':
    unittest.main()
