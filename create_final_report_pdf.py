"""
Script to create a professional PDF report from the final report markdown
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import re

# Define colors
BLUE = colors.HexColor('#1E3A8A')
DARK_BLUE = colors.HexColor('#1E40AF')
GRAY = colors.HexColor('#6B7280')

class FinalReportPDF:
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        self.story = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        def add_style_if_not_exists(name, style):
            try:
                self.styles.add(style)
            except KeyError:
                pass
        
        add_style_if_not_exists('ReportTitle', ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=BLUE,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        add_style_if_not_exists('SectionTitle', ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=DARK_BLUE,
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        add_style_if_not_exists('SubsectionTitle', ParagraphStyle(
            name='SubsectionTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=DARK_BLUE,
            spaceAfter=10,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        add_style_if_not_exists('BodyText', ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            leading=14
        ))

    def clean_text(self, text):
        """Clean and format text for PDF"""
        # Remove markdown formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
        # Remove markdown headers
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        # Escape HTML entities
        text = text.replace('&', '&amp;')
        return text

    def add_title_page(self):
        """Add title page"""
        title = Paragraph("AlphaCare Insurance Solutions", self.styles['ReportTitle'])
        self.story.append(Spacer(1, 2*inch))
        self.story.append(title)
        
        subtitle = Paragraph(
            "Data-Driven Risk Analytics & Premium Optimization",
            ParagraphStyle(
                name='Subtitle',
                parent=self.styles['Normal'],
                fontSize=16,
                textColor=GRAY,
                alignment=TA_CENTER,
                spaceAfter=30
            )
        )
        self.story.append(Spacer(1, 0.3*inch))
        self.story.append(subtitle)
        
        self.story.append(Spacer(1, 1.5*inch))
        
        info_text = """
        <b>Final Report</b><br/><br/>
        A Comprehensive Analysis of Insurance Claims Data<br/>
        to Identify Low-Risk Segments and Optimize Pricing Strategy<br/><br/><br/>
        <b>Prepared by:</b> ACIS Data Analytics Team<br/>
        <b>Date:</b> """ + datetime.now().strftime("%B %d, %Y") + """<br/>
        <b>Version:</b> 1.0
        """
        info = Paragraph(info_text, ParagraphStyle(
            name='Info',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        self.story.append(info)
        self.story.append(PageBreak())

    def add_content(self):
        """Add main content"""
        try:
            with open('reports/final_report.md', 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            content = "Final report content not found."
        
        # Split by major sections
        sections = re.split(r'\n## ', content)
        
        for i, section in enumerate(sections):
            if not section.strip():
                continue
            
            lines = section.split('\n')
            if not lines:
                continue
                
            # First line is usually the title
            title = lines[0].strip('#').strip()
            body_lines = lines[1:]
            
            # Skip if it's just the title line
            if i == 0 and not body_lines:
                continue
            
            # Add section title
            if title and i > 0:
                self.story.append(Paragraph(title, self.styles['SectionTitle']))
            
            # Process body
            current_para = []
            for line in body_lines:
                line = line.strip()
                
                if not line:
                    if current_para:
                        para_text = ' '.join(current_para)
                        para_text = self.clean_text(para_text)
                        if para_text:
                            self.story.append(Paragraph(para_text, self.styles['BodyText']))
                        current_para = []
                    continue
                
                # Handle bullet points
                if line.startswith('- ') or line.startswith('* '):
                    if current_para:
                        para_text = ' '.join(current_para)
                        para_text = self.clean_text(para_text)
                        if para_text:
                            self.story.append(Paragraph(para_text, self.styles['BodyText']))
                        current_para = []
                    bullet_text = line[2:].strip()
                    bullet_text = self.clean_text(bullet_text)
                    self.story.append(Paragraph(f"&bull; {bullet_text}", self.styles['BodyText']))
                # Handle subsections
                elif line.startswith('###'):
                    if current_para:
                        para_text = ' '.join(current_para)
                        para_text = self.clean_text(para_text)
                        if para_text:
                            self.story.append(Paragraph(para_text, self.styles['BodyText']))
                        current_para = []
                    sub_title = line.strip('#').strip()
                    self.story.append(Paragraph(sub_title, self.styles['SubsectionTitle']))
                else:
                    current_para.append(line)
            
            # Add remaining paragraph
            if current_para:
                para_text = ' '.join(current_para)
                para_text = self.clean_text(para_text)
                if para_text:
                    self.story.append(Paragraph(para_text, self.styles['BodyText']))
            
            self.story.append(Spacer(1, 0.2*inch))
            
            # Page break every few sections
            if i > 0 and i % 4 == 0:
                self.story.append(PageBreak())

    def add_header_footer(self, canvas_obj, doc):
        """Add header and footer"""
        canvas_obj.saveState()
        width, height = A4
        
        canvas_obj.setFont('Helvetica', 9)
        canvas_obj.setFillColor(GRAY)
        canvas_obj.drawString(72, height - 50, "ACIS Risk Analytics - Final Report")
        
        page_num = canvas_obj.getPageNumber()
        canvas_obj.drawCentredString(width / 2, 30, f"Page {page_num}")
        canvas_obj.drawString(width - 144, 30, datetime.now().strftime("%Y-%m-%d"))
        
        canvas_obj.restoreState()

    def build(self):
        """Build the PDF"""
        self.add_title_page()
        self.add_content()
        self.doc.build(self.story, onFirstPage=self.add_header_footer, 
                      onLaterPages=self.add_header_footer)

def main():
    """Generate the final report PDF"""
    output_filename = "ACIS_Final_Report.pdf"
    
    print(f"Creating final report PDF: {output_filename}")
    print("This may take a moment...")
    
    try:
        generator = FinalReportPDF(output_filename)
        generator.build()
        
        if os.path.exists(output_filename):
            size_kb = os.path.getsize(output_filename) / 1024
            print(f"\nPDF created successfully: {output_filename}")
            print(f"File location: {os.path.abspath(output_filename)}")
            print(f"File size: {size_kb:.2f} KB")
            return output_filename
        else:
            print("PDF file was not created.")
            return None
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None

if __name__ == "__main__":
    main()
