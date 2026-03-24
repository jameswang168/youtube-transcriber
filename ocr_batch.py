"""
批量 OCR 识别《邵子神数条文通行版》图片，生成纯文本文档
"""
import easyocr
import numpy as np
from PIL import Image
from pathlib import Path
import sys

img_dir = Path(r'C:\Users\james\OneDrive\桌面\油管视频处理\邵子神数条文\邵子神数条文通行版')
out_file = Path(r'C:\Users\james\OneDrive\桌面\油管视频处理\邵子神数条文\邵子神数条文通行版_OCR.txt')

imgs = sorted(img_dir.glob('*.png'))
print(f'共 {len(imgs)} 张图片，开始 OCR（CPU 模式，请耐心等待）...')

reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)

with open(out_file, 'w', encoding='utf-8') as f:
    f.write('《邵子神数条文》通行版 OCR 提取文本\n')
    f.write('=' * 60 + '\n\n')

    for i, img_path in enumerate(imgs):
        print(f'[{i+1:03d}/{len(imgs)}] 处理: {img_path.name}', flush=True)
        try:
            img_pil = Image.open(img_path).convert('RGB')
            img_np = np.array(img_pil)
            result = reader.readtext(img_np, detail=0, paragraph=True)

            f.write(f'\n【图片 {i+1}: {img_path.name}】\n')
            f.write('-' * 40 + '\n')
            for line in result:
                line = line.strip()
                if line:
                    f.write(line + '\n')
            f.flush()
        except Exception as e:
            print(f'  错误: {e}', flush=True)
            f.write(f'  [OCR失败: {e}]\n')

print(f'\n完成！输出文件: {out_file}')
