"""
Export PowerPoint Presentation to PDF
Automatically converts .pptx to .pdf using COM automation on Windows

Author: Son Nguyen
"""

import os
import sys

def export_pptx_to_pdf():
    """Export PowerPoint to PDF using COM automation"""
    try:
        # Try using win32com (Windows only)
        import win32com.client
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        
        pptx_path = os.path.join(project_dir, 'IBM_Capstone_Presentation.pptx')
        pdf_path = os.path.join(project_dir, 'IBM_Capstone_Presentation.pdf')
        
        if not os.path.exists(pptx_path):
            print(f"Error: File not found: {pptx_path}")
            return False
        
        print("Opening PowerPoint application...")
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = 1
        
        print(f"Opening presentation: {pptx_path}")
        presentation = powerpoint.Presentations.Open(os.path.abspath(pptx_path))
        
        print(f"Exporting to PDF: {pdf_path}")
        # Export as PDF (format type 32)
        presentation.SaveAs(os.path.abspath(pdf_path), 32)  # 32 = ppSaveAsPDF
        
        print("Closing presentation...")
        presentation.Close()
        
        print("Quitting PowerPoint...")
        powerpoint.Quit()
        
        # Delete PPTX file
        print(f"Deleting PPTX file: {pptx_path}")
        os.remove(pptx_path)
        
        print(f"\nSuccessfully exported to PDF: {pdf_path}")
        print(f"Deleted PPTX file")
        return True
        
    except ImportError:
        print("win32com not available. Trying alternative method...")
        return try_alternative_method()
    except Exception as e:
        print(f"Error with win32com: {e}")
        print("Trying alternative method...")
        return try_alternative_method()

def try_alternative_method():
    """Alternative method using subprocess"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        
        pptx_path = os.path.join(project_dir, 'IBM_Capstone_Presentation.pptx')
        pdf_path = os.path.join(project_dir, 'IBM_Capstone_Presentation.pdf')
        
        if not os.path.exists(pptx_path):
            print(f"Error: File not found: {pptx_path}")
            return False
        
        # Try using LibreOffice
        import subprocess
        
        print("Attempting to use LibreOffice...")
        cmd = [
            'soffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', project_dir,
            pptx_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(pdf_path):
            # Delete PPTX file
            print(f"Deleting PPTX file: {pptx_path}")
            os.remove(pptx_path)
            
            print(f"\n✓ Successfully exported to PDF: {pdf_path}")
            print(f"✓ Deleted PPTX file")
            return True
        else:
            print("LibreOffice not found or failed.")
            print("\nPlease export manually:")
            print(f"1. Open {pptx_path} in PowerPoint")
            print("2. File → Save As → PDF")
            print(f"3. Save as {pdf_path}")
            print(f"4. Delete {pptx_path}")
            return False
            
    except Exception as e:
        print(f"Alternative method failed: {e}")
        print("\nPlease export manually:")
        print(f"1. Open {pptx_path} in PowerPoint")
        print("2. File → Save As → PDF")
        print(f"3. Save as {pdf_path}")
        print(f"4. Delete {pptx_path}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Exporting PowerPoint to PDF")
    print("=" * 60)
    
    success = export_pptx_to_pdf()
    
    if success:
        print("\n" + "=" * 60)
        print("Export completed successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Automatic export failed. Please use manual method.")
        print("=" * 60)

