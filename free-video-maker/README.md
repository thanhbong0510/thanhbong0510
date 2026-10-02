# Free Video Maker: làm video hoạt hình 2D vi lịch sử, 100% miễn phí

Không cần ElevenLabs Pro hay Canva Pro. Bạn viết kịch bản vào `scenes.json`, chạy 1 lệnh là ra file MP4 1080p gồm:

- 🎙️ **Giọng đọc Mỹ tự nhiên**: Microsoft Edge TTS (miễn phí, không cần key) hoặc Kokoro (mã nguồn mở)
- 🎨 **Hình 2D cùng một phong cách** cho mọi cảnh: Pollinations.ai (miễn phí, không cần key)
- 🎬 **Chuyển động**: zoom/pan mượt kiểu Ken Burns, chuyển cảnh mờ dần
- 💬 **Phụ đề** tự khớp với giọng đọc, có thể thêm **nhạc nền** tuỳ chọn

## Cài đặt (1 lần)

1. Cài **Python 3.10+**: https://www.python.org/downloads/ (Windows: tích ô "Add Python to PATH")
2. Cài **ffmpeg**:
   - Windows: `winget install ffmpeg`
   - Mac: `brew install ffmpeg`
3. Cài thư viện giọng đọc:
   ```
   pip install edge-tts
   ```

## Chạy

```
cd free-video-maker
python make_video.py scenes.json --out paperclip.mp4
```

Thêm nhạc nền (tải nhạc miễn phí từ YouTube Audio Library hoặc Pixabay Music):
```
python make_video.py scenes.json --music nhac.mp3 --out paperclip.mp4
```

Chạy thử không cần mạng (ảnh giả, không có tiếng) để kiểm tra máy đã cài đủ chưa:
```
python make_video.py scenes.json --mock
```

## Viết kịch bản trong `scenes.json`

```json
{
  "style": "flat 2D vector illustration, vintage American storybook style, ...",
  "voice": "en-US-AndrewNeural",
  "scenes": [
    { "text": "Lời đọc tiếng Anh", "image": "mô tả hình bằng tiếng Anh", "motion": "zoom_in" },
    { "text": "...", "image_file": "anh_tu_library_of_congress.jpg", "motion": "pan_right" }
  ]
}
```

| Trường | Ý nghĩa |
|---|---|
| `style` | Phong cách chung, tự gắn vào đầu mọi prompt ảnh nên các cảnh luôn đồng bộ. **Giữ cố định cho cả kênh.** |
| `voice` | Giọng Edge TTS (xem bảng dưới) |
| `rate` | Tốc độ đọc, ví dụ `"-5%"` (chậm hơn một chút, hợp kể chuyện) |
| `seed` | Đổi số này nếu không thích ảnh, chạy lại sẽ ra ảnh khác |
| `text` | Lời đọc của cảnh. Mỗi cảnh **1–2 câu (5–8 giây)** để hình đổi liên tục |
| `image` | Mô tả hình của cảnh |
| `image_file` | Dùng ảnh có sẵn (ví dụ ảnh public domain từ Library of Congress) thay cho ảnh AI |
| `motion` | `zoom_in`, `zoom_out`, `pan_left`, `pan_right`, `pan_up`, `pan_down` |

**Mẹo:** xen kẽ các kiểu `motion` khác nhau giữa các cảnh để video không bị đơn điệu.

## Giọng đọc gợi ý (Edge TTS, giọng Mỹ)

| Giọng | Đặc điểm |
|---|---|
| `en-US-AndrewNeural` | Nam, ấm, kiểu kể chuyện (mặc định) |
| `en-US-ChristopherNeural` | Nam, trầm, nghiêm túc kiểu phim tài liệu |
| `en-US-BrianNeural` | Nam, trẻ, thân thiện |
| `en-US-AvaNeural` | Nữ, ấm, rõ ràng |
| `en-US-EmmaNeural` | Nữ, vui tươi |

Xem toàn bộ giọng: `edge-tts --list-voices`

## Sửa một cảnh mà không làm lại cả video

Giọng và ảnh được lưu trong thư mục `work/`. Muốn làm lại cảnh 3 thì xoá `work/scene_002.jpg` (hoặc `.mp3`) rồi chạy lại lệnh. Chỉ cảnh đó được tạo mới.

## ⚠️ Lưu ý khi bật kiếm tiền YouTube

- **Edge TTS** dùng dịch vụ đọc của trình duyệt Microsoft Edge, không phải sản phẩm thương mại chính thức. Nhiều kênh vẫn dùng nhưng có rủi ro. Khi kênh bắt đầu kiếm tiền, nên chuyển sang **Kokoro** (giấy phép Apache 2.0, dùng thương mại thoải mái, chạy trên máy bạn):
  ```
  pip install kokoro soundfile
  python make_video.py scenes.json --tts kokoro
  ```
  (Windows cần cài thêm espeak-ng: https://github.com/espeak-ng/espeak-ng/releases)
- **Pollinations**: đọc điều khoản tại https://pollinations.ai trước khi kiếm tiền. Ảnh lịch sử từ Library of Congress / NARA (dùng qua `image_file`) là public domain, an toàn nhất.
- YouTube yêu cầu nội dung có **giá trị riêng**: kịch bản do bạn viết, có nghiên cứu. Đừng chỉ ghép ảnh AI với giọng máy một cách hàng loạt.

## Nâng cấp thêm (đều miễn phí)

- **Cảnh cử động thật** (nhân vật đi, nói): đưa ảnh trong `work/` vào **Kling AI** hoặc **Hailuo AI** (có credit miễn phí hằng ngày) để tạo clip 5 giây, rồi ghép vào bằng CapCut.
- **Chữ động, mốc năm, bản đồ**: **CapCut** (bản miễn phí có keyframe và hiệu ứng chữ).
- **Hiệu ứng âm thanh**: https://freesound.org, https://pixabay.com/sound-effects/
