import easyocr
import numpy as np
from PIL import Image
from pathlib import Path

img_dir = Path(r'C:\Users\james\OneDrive\桌面\油管视频处理\邵子神数条文\邵子神数条文通行版')

imgs = sorted(img_dir.glob('*.png'))
print(f'共找到 {len(imgs)} 张图片')
print(f'测试图片: {imgs[0].name}')

reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)

# 用 PIL 读取（绕过中文路径问题），转为 numpy array
img_pil = Image.open(imgs[0]).convert('RGB')
img_np = np.array(img_pil)

result = reader.readtext(img_np, detail=0, paragraph=True)

print('\n=== OCR 结果预览（前30行）===')
for line in result[:30]:
    print(line)
