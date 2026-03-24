# YouTube 视频语音转文字工具

输入 YouTube 视频链接，自动下载音频并使用本地 Whisper 模型转录为文字，结果在网页中展示。**全程本地运行，无需 API Key，无需联网调用 AI 服务。**

---

## 功能特性

- 粘贴 YouTube 链接，一键开始处理
- 实时显示进度（下载 → 转录 → 生成文档）
- 转录结果带时间戳（`[00:12 → 00:18]` 格式）
- 支持多种 Whisper 模型（tiny / base / small / medium / large）
- 支持自动语言检测或手动指定语言
- 历史记录自动保存，可随时查看
- 网页内嵌 YouTube 播放器，对照字幕回放

---

## 目录结构

```
youtube-transcriber/
├── yt-dlp.exe                  # YouTube 下载工具（需手动下载，见下文）
├── webapp/
│   ├── app.py                  # Flask 后端主程序
│   ├── 启动服务.bat             # 一键启动脚本
│   ├── templates/
│   │   └── index.html          # 前端页面
│   └── results/                # 转录结果存放目录（自动创建）
├── whisper_transcribe.py       # 命令行版转录脚本
├── download_and_transcribe.bat # 命令行版一键脚本
├── ocr_batch.py                # 批量图片 OCR 脚本
├── pdf_extract.py              # PDF 文字提取脚本
└── .gitignore
```

---

## 安装步骤

### 第一步：安装 Python

1. 打开 https://www.python.org/downloads/
2. 下载 **Python 3.10 或 3.11**（推荐 3.11）
3. 运行安装程序，**务必勾选 "Add Python to PATH"**，然后点击 Install Now
4. 安装完成后，打开命令提示符（Win + R → 输入 `cmd` → 回车），验证：
   ```
   python --version
   ```
   显示版本号即为成功。

---

### 第二步：下载 yt-dlp.exe

1. 打开 https://github.com/yt-dlp/yt-dlp/releases/latest
2. 下载 `yt-dlp.exe`
3. 将 `yt-dlp.exe` 放到项目根目录（与 `webapp/` 同级）

---

### 第三步：安装 ffmpeg

Whisper 转录音频时依赖 ffmpeg，必须安装。

**方法一：通过 winget 安装（推荐，Win10/11 自带 winget）**

打开命令提示符，运行：
```
winget install --id Gyan.FFmpeg -e --source winget
```
安装完成后**关闭并重新打开**命令提示符，验证：
```
ffmpeg -version
```

**方法二：手动安装**

1. 打开 https://www.gyan.dev/ffmpeg/builds/
2. 下载 `ffmpeg-release-essentials.zip`
3. 解压到 `C:\ffmpeg\`
4. 将 `C:\ffmpeg\bin` 添加到系统环境变量 PATH：
   - 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
   - 在"系统变量"中找到 `Path`，双击 → 新建 → 输入 `C:\ffmpeg\bin`
   - 点击确定，重新打开命令提示符验证

---

### 第四步：安装 Python 依赖库

打开命令提示符，逐条运行以下命令：

```
pip install flask
pip install openai-whisper
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

> **说明：**
> - `flask`：Web 服务框架
> - `openai-whisper`：语音转文字模型（本地推理，不联网）
> - `torch`：Whisper 的运行依赖，上面命令安装 CPU 版本（约 200MB）
>
> **如果你有 NVIDIA 显卡**，可以安装 GPU 版 torch，速度会快 5-10 倍：
> ```
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
> ```
> （cu121 对应 CUDA 12.1，根据你的显卡驱动版本选择）

---

### 第五步：下载 Whisper 模型（首次运行自动下载）

首次运行时，Whisper 会自动从 OpenAI 官方下载模型文件到本机缓存目录  
（`C:\Users\你的用户名\.cache\whisper\`），**之后无需重复下载**。

各模型大小与速度对比：

| 模型 | 文件大小 | 转录速度 | 推荐场景 |
|------|---------|---------|---------|
| tiny | 75 MB | 最快 | 快速测试 |
| base | 142 MB | 快 | 英文内容 |
| small | 466 MB | 中 | 一般使用 |
| **medium** | **1.4 GB** | **慢** | **中文推荐** |
| large | 2.9 GB | 最慢 | 最高精度 |

> 中文视频建议使用 **medium** 或 **large** 模型，tiny/base 对中文识别效果较差。

---

## 启动网页应用

安装完成后，有两种方式启动：

**方式一：双击批处理文件**

双击项目目录中的 `webapp\启动服务.bat`

**方式二：命令行启动**

```
cd webapp
python app.py
```

启动成功后，打开浏览器访问：

```
http://127.0.0.1:5000
```

---

## 使用方法

1. 在网页输入框中粘贴 YouTube 视频链接
2. 选择 Whisper 模型（中文视频推荐 medium）
3. 选择语言（中文选 `zh`，不确定选 `auto`）
4. 点击"开始处理"
5. 等待进度条完成（时长约为视频时长的 1-3 倍，取决于电脑性能）
6. 查看带时间戳的转录结果

---

## 常见问题

**Q: 提示 `ffmpeg not found`**  
A: ffmpeg 未正确加入 PATH，参考第三步，安装后重新打开命令提示符再试。

**Q: 首次运行很慢，卡在"加载模型"**  
A: 正在自动下载模型文件，medium 模型约 1.4GB，请耐心等待，下载完成后下次启动会很快。

**Q: 转录速度很慢**  
A: CPU 模式下 medium 模型处理 1 小时视频约需 2-4 小时。有 NVIDIA 显卡的用户安装 GPU 版 torch 可大幅提速。

**Q: 中文识别错误较多**  
A: 尝试换用更大的模型（medium → large），或在启动时指定语言为 `zh`。

**Q: `pip install` 提示网络错误**  
A: 使用国内镜像加速：
```
pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install openai-whisper -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-03-24 | 初始发布，支持 Web 界面、实时进度、历史记录 |

---

## 许可证

MIT License — 自由使用、修改、分发。
