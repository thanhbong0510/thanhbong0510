# Free Video Maker: làm video hoạt hình 2D vi lịch sử, 100% miễn phí

Bạn viết kịch bản vào `scenes.json`, chạy 1 lệnh là ra file MP4 1080p gồm:

- 🎙️ **Giọng đọc Mỹ tự nhiên**: Kokoro (chạy trên máy, được dùng thương mại) hoặc Edge TTS
- 🎨 **Hình 2D cùng một phong cách** cho mọi cảnh: Stable Diffusion chạy trên máy (không giới hạn) hoặc Pollinations.ai (online)
- 🎬 **Chuyển động**: hiệu ứng **2.5D** (camera lượn, vật gần di chuyển nhiều hơn vật xa) và zoom/pan kiểu Ken Burns
- 💬 **Phụ đề** tự khớp với giọng đọc, có thể thêm **nhạc nền**

Đã điều chỉnh cho máy **Windows 10, GTX 1070 8GB, RAM 64GB**.

## Cài đặt (1 lần)

1. Cập nhật **driver NVIDIA** mới nhất: https://www.nvidia.com/Download/index.aspx
2. Cài **Python 3.11**: https://www.python.org/downloads/release/python-3119/. Khi cài, **tích ô "Add Python to PATH"**.
3. Nháy đúp **`install_windows.bat`**. Script tự cài ffmpeg, PyTorch (bản hợp với GTX 1070) và các thư viện. Mất khoảng 10–20 phút.
4. Nếu dòng cuối hiện `GPU OK: NVIDIA GeForce GTX 1070` là xong.
5. (Khuyên dùng, cho giọng Kokoro) Cài **espeak-ng**: tải file `.msi` tại https://github.com/espeak-ng/espeak-ng/releases

## Chạy

Mở cửa sổ lệnh (cmd) trong thư mục `free-video-maker`:

```
run.bat scenes.json --out paperclip.mp4
```

| Lệnh | Tác dụng |
|---|---|
| `run.bat scenes.json --tts kokoro --images sd` | **Chạy hoàn toàn trên máy**: không giới hạn, không phụ thuộc dịch vụ nào |
| `run.bat scenes.json --music nhac.mp3` | Thêm nhạc nền (tải từ YouTube Audio Library / Pixabay Music) |
| `run.bat scenes.json --no-subs` | Không chèn phụ đề vào hình (tự tải file `work/subs.srt` lên YouTube) |
| `run.bat scenes.json --mock` | Chạy thử không cần mạng/GPU để kiểm tra cài đặt |

Lần đầu dùng `--images sd`, máy sẽ tải model Stable Diffusion (khoảng 7GB).

### Thời gian ước tính trên GTX 1070 (ước lượng, chưa đo trên máy bạn)

| Việc | Thời gian |
|---|---|
| SDXL (`"sd_type": "sdxl"`) | ~2–4 phút/ảnh, video 70 cảnh ≈ 3–4 tiếng → **để chạy qua đêm** |
| SD 1.5 (`"sd_type": "sd15"`) | ~20–40 giây/ảnh, nhanh hơn nhiều nhưng ảnh kém đẹp hơn |
| Giọng Kokoro trên CPU Xeon | Nhanh hơn thời gian thực |
| Hiệu ứng 2.5D + ghép video | ~1–2 phút cho 1 phút video |

Ảnh và giọng đã tạo được lưu trong `work/`. Nếu bị dừng giữa chừng, chạy lại sẽ **làm tiếp từ chỗ dừng**.

## Viết kịch bản trong `scenes.json`

```json
{
  "style": "phong cách ảnh (dùng cho Pollinations)",
  "sd_style": "phong cách ảnh ngắn gọn (dùng cho Stable Diffusion)",
  "tts": "kokoro",
  "images": "sd",
  "scenes": [
    { "text": "Lời đọc tiếng Anh", "image": "mô tả hình bằng tiếng Anh", "motion": "parallax_in" },
    { "text": "...", "image_file": "anh_tu_library_of_congress.jpg" }
  ]
}
```

| Trường | Ý nghĩa |
|---|---|
| `style` / `sd_style` | Phong cách chung gắn vào mọi prompt ảnh. **Giữ cố định cho cả kênh.** `sd_style` nên ngắn (dưới ~40 từ) vì Stable Diffusion chỉ đọc được khoảng 75 từ khoá |
| `negative` | Những thứ không muốn xuất hiện trong ảnh |
| `tts` | `kokoro` hoặc `edge` |
| `voice` / `kokoro_voice` | Giọng đọc (xem bảng dưới) |
| `rate` | Tốc độ Edge TTS, ví dụ `"-5%"` |
| `images` | `sd` (trên máy) hoặc `pollinations` (online) |
| `sd_type` | `sdxl` (đẹp, chậm) hoặc `sd15` (nhanh) |
| `sd_model` | Để trống thì dùng model gốc. Hoặc điền đường dẫn file `.safetensors` tải từ Civitai |
| `sd_lora`, `sd_lora_scale` | Đường dẫn file LoRA phong cách 2D, độ mạnh từ 0.6 đến 1.0 |
| `sd_steps`, `sd_cfg` | Số bước (20–30) và độ bám prompt (5–8) |
| `seed` | Đổi số này để ra bộ ảnh khác |
| `text` | Lời đọc của cảnh. Mỗi cảnh **1–2 câu (5–8 giây)** |
| `image` | Mô tả hình |
| `image_file` | Dùng ảnh có sẵn (ảnh public domain từ Library of Congress, NARA...). **Rất hợp với hiệu ứng 2.5D** |
| `motion` | Bỏ trống thì **tự xoay vòng** các kiểu để cảnh nào cũng khác nhau |

### Các kiểu chuyển động

| `motion` | Hiệu ứng |
|---|---|
| `parallax_in` | 2.5D: camera tiến vào, tiền cảnh phóng to nhanh hơn hậu cảnh |
| `parallax_left` / `parallax_right` | 2.5D: camera lượn ngang, có chiều sâu |
| `parallax_up` | 2.5D: camera nâng lên |
| `zoom_in` / `zoom_out` | Phóng to / thu nhỏ phẳng |
| `pan_left` / `pan_right` / `pan_up` / `pan_down` | Lia máy phẳng |

Hiệu ứng 2.5D dùng model **Depth Anything V2** để đoán độ xa gần của từng điểm ảnh. Model này tự tải lần đầu (khoảng 100MB).

### Mẹo chọn model ảnh 2D trên Civitai
- Tìm theo từ khoá: `flat illustration`, `storybook`, `vintage illustration`, `cartoon` và lọc theo **SDXL** hoặc **SD 1.5**.
- **Kiểm tra giấy phép**: mục "Commercial use" phải cho phép dùng trên ảnh được tạo ra (*generated images*).
- Tải file `.safetensors`, đặt vào thư mục `models/` rồi điền `"sd_model": "models/ten_file.safetensors"`.

## Giọng đọc gợi ý

| Kokoro (`kokoro_voice`) | Edge TTS (`voice`) | Đặc điểm |
|---|---|---|
| `am_michael` | `en-US-AndrewNeural` | Nam, ấm, kể chuyện |
| `am_fenrir` | `en-US-ChristopherNeural` | Nam, trầm, kiểu phim tài liệu |
| `af_heart` | `en-US-AvaNeural` | Nữ, ấm, rõ ràng |
| `af_bella` | `en-US-EmmaNeural` | Nữ, tươi sáng |

## Sửa một cảnh mà không làm lại cả video

Xoá file của cảnh đó trong `work/` (ví dụ cảnh 3 là `scene_002.png` hoặc `scene_002.mp3`) rồi chạy lại. Chỉ cảnh đó được tạo mới.

## ⚠️ Lưu ý khi bật kiếm tiền YouTube

- Dùng **Kokoro** (giấy phép Apache 2.0) thay cho Edge TTS. Edge TTS không phải dịch vụ thương mại chính thức.
- **SDXL / SD 1.5 gốc**: giấy phép OpenRAIL cho phép dùng thương mại ảnh tạo ra. Model tải từ Civitai thì xem giấy phép của từng model.
- Ảnh từ Library of Congress / NARA (qua `image_file`) là public domain, an toàn nhất.
- YouTube yêu cầu nội dung có **giá trị riêng**: kịch bản do bạn nghiên cứu và viết. Không nên làm hàng loạt.

## Lỗi thường gặp

| Lỗi | Cách sửa |
|---|---|
| `no kernel image is available for execution on the device` | PyTorch bản quá mới không hỗ trợ GTX 1070. Chạy lại `install_windows.bat` |
| `CUDA out of memory` | Đổi `"sd_type": "sd15"`, hoặc tắt bớt chương trình dùng GPU (trình duyệt, game) |
| Ảnh SDXL ra màu đen | Đã xử lý sẵn bằng VAE fp16-fix. Nếu vẫn bị, báo lại cho tôi |
| `'ffmpeg' is not recognized` | Đóng cửa sổ cmd, mở lại sau khi cài |
