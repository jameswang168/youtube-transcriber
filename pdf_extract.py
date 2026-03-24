import fitz
from pathlib import Path

pdf_path = Path(r'C:\Users\james\OneDrive\桌面\油管视频处理\邵子神数条文\VY3cPcpwSd.pdf')
out_path = Path(r'C:\Users\james\OneDrive\桌面\油管视频处理\邵子神数条文\VY3cPcpwSd_提取文字.txt')

doc = fitz.open(str(pdf_path))
total = len(doc)
text_pages = 0
img_pages = 0

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(f'《邵子神数条文》PDF 文字提取\n')
    f.write(f'来源: {pdf_path.name} | 共 {total} 页\n')
    f.write('=' * 60 + '\n\n')
    for i in range(total):
        page = doc[i]
        text = page.get_text().strip()
        if text:
            text_pages += 1
            f.write(f'--- 第{i+1}页 ---\n{text}\n\n')
        else:
            img_pages += 1

doc.close()

size = out_path.stat().st_size / 1024
print(f'完成！共 {total} 页')
print(f'  有文字页: {text_pages} 页')
print(f'  纯图片页: {img_pages} 页')
print(f'  输出文件: {out_path.name} ({size:.1f} KB)')
