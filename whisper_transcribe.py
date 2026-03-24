import whisper
import os

wav = r'C:\Users\james\OneDrive\桌面\油管视频处理\视频\7BtVrfUe0QY.wav'
out = r'C:\Users\james\OneDrive\桌面\油管视频处理\视频\7BtVrfUe0QY_transcript.txt'

print('加载 Whisper medium 模型（首次运行需下载约1.4GB，请耐心等待）...')
model = whisper.load_model('medium')

print('开始转录，语言：中文...')
result = model.transcribe(wav, language='zh', verbose=True)

with open(out, 'w', encoding='utf-8') as f:
    f.write('《邵子神数》视频语音转文字\n')
    f.write('视频ID: 7BtVrfUe0QY\n')
    f.write('=' * 60 + '\n\n')
    # 写带时间戳的分段
    for seg in result['segments']:
        t_start = seg['start']
        t_end   = seg['end']
        text    = seg['text'].strip()
        m_s, s_s = divmod(int(t_start), 60)
        m_e, s_e = divmod(int(t_end), 60)
        f.write(f'[{m_s:02d}:{s_s:02d} --> {m_e:02d}:{s_e:02d}] {text}\n')
    f.write('\n' + '=' * 60 + '\n')
    f.write('【纯文字版】\n\n')
    f.write(result['text'])

print(f'\n转录完成！输出文件: {out}')
input('按 Enter 关闭窗口...')
