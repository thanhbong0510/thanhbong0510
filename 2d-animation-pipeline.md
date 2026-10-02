# Quy trình làm video vi lịch sử Mỹ dạng hoạt hình 2D

Mục tiêu: **chuyển động 2D + giọng đọc hay + cảnh phong phú, khớp với câu chuyện**.
★ = công cụ đã kết nối sẵn trong Claude (gọi được ngay, không cần tự đăng ký API).

## Bộ công cụ theo từng việc

### 1. Giọng đọc (quan trọng nhất cho khán giả Mỹ)

| Công cụ | Ghi chú | Link |
|---|---|---|
| ★ **ElevenLabs** | Giọng Mỹ tự nhiên nhất, kiểu kể chuyện tài liệu. Có thể tạo giọng riêng cho kênh | https://elevenlabs.io/docs |
| ★ vidIQ Voiceover | Phương án dự phòng | — |
| IBM Text to Speech / Audexum | Rẻ hơn nhưng giọng kém tự nhiên hơn | (public-apis) |

Gợi ý giọng: nam hoặc nữ trầm, ấm, tốc độ ~150 từ/phút, kiểu "storyteller / documentary".

### 2. Hình minh hoạ 2D (cảnh, nhân vật)

| Công cụ | Ghi chú |
|---|---|
| ★ **ElevenLabs Image** | Tạo ảnh 2D theo kịch bản, giữ phong cách đồng nhất nhờ dùng chung một "style prompt" |
| ★ **Canva generate-image / design** | Tạo cảnh nhanh, có sẵn template, chữ |
| Kavel (public-apis) | Tạo ảnh AI miễn phí, không cần key |
| Library of Congress / NARA / Smithsonian | Ảnh lịch sử **thật** → biến thành 2D bằng cách tách lớp (mục 4) |

**Style prompt cố định cho cả kênh** (dán vào đầu mọi prompt ảnh để các cảnh đồng bộ):
```
flat 2D vector illustration, vintage American storybook style, muted warm palette
(cream, mustard, teal, brick red), subtle paper grain texture, clean outlines,
simple expressive characters, 16:9, no text
```
Ví dụ cảnh: `[style prompt], a 1900s New York patent office, a clerk stamping papers, sunlight through tall windows`

### 3. Làm cho hình chuyển động

| Cách | Công cụ | Dùng khi |
|---|---|---|
| Ảnh → video ngắn (3–8 giây) | ★ **ElevenLabs Video** (image-to-video), KPainter (public-apis) | Cảnh nhân vật cử động, đám đông, máy móc chạy |
| Chữ động, số đếm, mốc năm, biểu đồ | ★ **vidIQ Motion Graphics** | "1899", "$1 million", so sánh trước/sau |
| Icon động | Lordicon, LottieFiles (★ ngoài danh sách) | Bóng đèn bật, đồng hồ quay, mũi tên chỉ |
| Pan/zoom (Ken Burns) | Shotstack, JSON2Video, CapCut | Ảnh tĩnh, bản đồ, trang báo cổ |

### 4. Hiệu ứng 2.5D (parallax) từ ảnh lịch sử thật

1. Lấy ảnh từ Library of Congress / NARA (public domain).
2. Làm nét: **UpRes** (public-apis).
3. Tách người khỏi nền: **Remove.bg / PhotoRoom** hoặc ★ **Canva remove-background**.
4. Đặt lớp người và lớp nền chuyển động ở tốc độ khác nhau → ra cảm giác 3D, rất hợp kiểu kênh lịch sử.

### 5. Âm thanh

| Công cụ | Dùng để |
|---|---|
| Freesound | SFX: máy đánh chữ, tiếng tàu hoả, đám đông, tiếng giấy |
| ★ vidIQ Generate Music | Nhạc nền không bản quyền theo tâm trạng |
| Archive.org (audio) | Ragtime, jazz thập niên 1920 đã hết bản quyền — đúng chất "Mỹ xưa" |

### 6. Ghép video

| Công cụ | Ghi chú |
|---|---|
| CapCut / DaVinci Resolve | Dựng tay, miễn phí |
| **Shotstack / JSON2Video** (public-apis) | Ghép tự động bằng JSON: ảnh + clip + giọng + phụ đề |
| Remotion (★ ngoài danh sách) | Dựng video bằng code React, miễn phí cho cá nhân |

---

## Quy trình 1 video (8–10 phút)

1. **Kịch bản** → chia thành **cảnh, mỗi cảnh 5–8 giây** (~60–90 cảnh). Mỗi cảnh ghi: lời đọc · hình · kiểu chuyển động · SFX.
2. **Giọng đọc** bằng ElevenLabs trước → biết chính xác độ dài từng cảnh.
3. **Hình**: tạo ảnh 2D bằng style prompt cố định; xen kẽ ảnh lịch sử thật (khoảng 30%) để tăng độ tin cậy.
4. **Chuyển động**:
   - ~30% cảnh: image-to-video (cảnh quan trọng, cao trào)
   - ~40% cảnh: pan/zoom + parallax (rẻ, nhanh)
   - ~30% cảnh: motion graphics (năm, số liệu, bản đồ, trích dẫn)
5. **SFX + nhạc** → **ghép** → phụ đề.

> Mẹo giữ chân người xem: cứ **3–5 giây đổi hình hoặc có chuyển động mới**, đừng để ảnh tĩnh quá 6 giây.

## Bảng cảnh mẫu (storyboard)

| # | Lời đọc | Hình | Chuyển động | SFX |
|---|---|---|---|---|
| 1 | "In 1899, a man walked into the patent office with a piece of bent wire…" | 2D: người đàn ông cầm kẹp giấy trước toà nhà cổ | Image-to-video: bước vào cửa | Tiếng bước chân, cửa gỗ |
| 2 | "…and it would end up on every desk in America." | Hàng nghìn kẹp giấy rơi xuống bàn | Motion graphic đếm số | "Ting" |
| 3 | "But here's the twist: he wasn't the inventor." | Bản vẽ bằng sáng chế gốc (USPTO) | Zoom chậm + vệt đỏ khoanh tròn | Nhạc dừng đột ngột |
