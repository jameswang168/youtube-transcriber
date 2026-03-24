import fitz  # pymupdf
from pathlib import Path

base = Path(r'C:\Users\james\OneDrive\桌面\油管视频处理\邵子神数条文')
pdfs = list(base.glob('*.pdf'))
print(f'找到 {len(pdfs)} 个PDF: {[p.name for p in pdfs]}')

for pdf_path in pdfs:
    doc = fitz.open(str(pdf_path))
    print(f'\n=== {pdf_path.name} | 共 {len(doc)} 页 ===')
    # 取前3页看看能不能提取文字
    for i in range(min(3, len(doc))):
        page = doc[i]
        text = page.get_text().strip()
        print(f'  第{i+1}页: {len(text)} 字符')
        if text:
            print(f'  预览: {text[:200]}')
        else:
            print(f'  [纯图片页，无可提取文字]')
    doc.close()
