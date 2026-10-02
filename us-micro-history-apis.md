# API cho kênh vi lịch sử Mỹ (US micro-history)

Phần lớn lấy từ [public-apis/public-apis](https://github.com/public-apis/public-apis). Mục nào có dấu ★ không nằm trong danh sách đó nhưng rất hợp với kênh này.
Ưu tiên nguồn **public domain / CC0** để video kiếm tiền an toàn trên YouTube.

## 1. Tìm ý tưởng & kiểm chứng sự thật

| API | Dùng để | Key | Link |
|---|---|---|---|
| Wikipedia (On This Day + REST) | Sự kiện theo ngày, tóm tắt bài viết, lấy ảnh đại diện | Không | https://api.wikimedia.org/wiki/Feed_API/Reference/On_this_day |
| SlashYear | 86.902 sự kiện lịch sử, mỗi cái trích từ Wikipedia có nguồn | Không | https://slashyear.com/api |
| Wikidata | Dữ kiện chính xác: ngày phát minh, người phát minh, năm sinh/mất | Không | https://www.wikidata.org/w/api.php?action=help |
| Random Useless Facts | Gợi ý chủ đề "sự thật lạ" (phải kiểm chứng lại) | Không | https://uselessfacts.jsph.pl/ |
| Black History Facts | Kho dữ kiện lịch sử người Mỹ gốc Phi (hợp tháng 2, Black History Month) | apiKey | https://www.blackhistoryapi.io/docs |

## 2. Phát minh & bằng sáng chế (chủ đề "ai phát minh ra X")

| API | Dùng để | Key | Link |
|---|---|---|---|
| PatentsView | Tra bằng sáng chế Mỹ: người phát minh, ngày cấp, công ty | apiKey (miễn phí) | https://patentsview.org/apis/purpose |
| USPTO Open Data | Dữ liệu và bản vẽ gốc của bằng sáng chế Mỹ | Không | https://developer.uspto.gov/ |

> Bản vẽ bằng sáng chế cũ (như kẹp giấy năm 1899, đèn giao thông năm 1923) là hình minh hoạ rất "ăn" cho kênh này.

## 3. Ảnh, báo cổ, phim tư liệu (B-roll lịch sử)

| API | Dùng để | Key | Link |
|---|---|---|---|
| ★ Library of Congress (loc.gov) | Ảnh, bản đồ, poster, báo cổ — thêm `?fo=json` vào URL bất kỳ | Không | https://www.loc.gov/apis/ |
| Chronicling America | Hàng triệu trang báo Mỹ 1756–1963 (đang chuyển sang loc.gov) | Không | https://chroniclingamerica.loc.gov/about/api/ |
| ★ National Archives (NARA) | Ảnh, tài liệu, phim của chính phủ Mỹ — gần như toàn bộ là public domain | apiKey | https://catalog.archives.gov/api/v2/api-docs/ |
| ★ DPLA | Tìm một lần qua hàng nghìn thư viện/bảo tàng Mỹ | apiKey | https://pro.dp.la/developers/api-codex |
| Archive.org | **Prelinger Archives**: phim quảng cáo/giáo dục Mỹ 1920–1970, nhiều phim public domain | Không | https://archive.readme.io/docs |
| Smithsonian Open Access | Hơn 5 triệu ảnh CC0 (Bảo tàng Lịch sử Mỹ, Hàng không Vũ trụ…) | apiKey (api.data.gov) | https://github.com/Smithsonian/smithsonian-openaccess |
| Metropolitan Museum of Art | Ảnh hiện vật, nhiều ảnh CC0 | Không | https://metmuseum.github.io/ |
| Art Institute of Chicago | Tranh Mỹ, ảnh CC0 | Không | https://api.artic.edu/docs/ |
| NYPL "What's on the menu?" | Thực đơn nhà hàng Mỹ từ thế kỷ 19 (chủ đề ẩm thực) | apiKey | http://nypl.github.io/menus-api/ |
| NASA Image Library | Ảnh/video Apollo, chạy đua vào không gian (public domain) | Không | https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf |

## 4. Dữ liệu chính phủ Mỹ (số liệu, biểu đồ, địa điểm)

| API | Dùng để | Key | Link |
|---|---|---|---|
| Census.gov | Dân số theo thời gian → biểu đồ trong video | Không | https://www.census.gov/data/developers/data-sets.html |
| National Park Service | Di tích, địa danh lịch sử kèm ảnh | apiKey | https://www.nps.gov/subjects/developer/ |
| Recreation.gov (RIDB) | Di tích lịch sử, bảo tàng liên bang | apiKey | https://ridb.recreation.gov/ |
| Federal Register | Văn bản luật/sắc lệnh Mỹ (chủ đề luật kỳ quặc) | Không | https://www.federalregister.gov/reader-aids/developer-resources/rest-api |
| MLB Records and Stats | Lịch sử bóng chày (chủ đề thể thao Mỹ) | Không | https://appac.github.io/mlb-data-api-docs/ |

## 5. Âm thanh, giọng đọc, dựng video

| API | Dùng để | Key | Link |
|---|---|---|---|
| Freesound | SFX: tiếng máy đánh chữ, máy chiếu phim, đám đông… | apiKey | https://freesound.org/docs/api/ |
| ★ Musopen / Archive.org audio | Nhạc cổ điển, ragtime, jazz đầu thế kỷ 20 đã hết bản quyền | Không | https://archive.org/details/audio |
| Pexels / Pixabay | B-roll hiện đại (cảnh nước Mỹ ngày nay) | apiKey | https://www.pexels.com/api/ |
| Shotstack / JSON2Video | Tự động ghép ảnh + giọng đọc + chữ thành video | apiKey | https://shotstack.io/ |

> Giọng đọc tiếng Anh giọng Mỹ: dùng ElevenLabs (đã kết nối sẵn) thay vì IBM TTS cho tự nhiên hơn.

---

## Quy trình gợi ý cho 1 video

1. **Chọn chủ đề**: Wikipedia On This Day / SlashYear → chọn sự kiện lạ.
2. **Kiểm chứng**: Wikidata (ngày tháng, tên) + PatentsView (nếu là phát minh) + Chronicling America (bài báo gốc thời đó — vừa là nguồn vừa là hình).
3. **Lấy hình**: loc.gov → NARA → Smithsonian → Archive.org (phim Prelinger).
4. **Âm thanh**: Freesound + nhạc public domain trên Archive.org.
5. **Ghép**: giọng đọc ElevenLabs + Shotstack/CapCut.

## Lưu ý bản quyền (quan trọng với YouTube)

- **Tác phẩm của chính phủ liên bang Mỹ** (NARA, NASA, NPS, quân đội) → public domain, dùng thoải mái.
- **Tác phẩm xuất bản ở Mỹ trước năm 1931** → public domain (từ 1/1/2026 mốc này là năm 1930 trở về trước).
- Library of Congress: chọn mục có ghi **"No known restrictions"** hoặc **"Free to use and reuse"**.
- Smithsonian/Met/AIC: chỉ dùng ảnh có nhãn **CC0 / Open Access**.
- Archive.org: không phải tất cả đều public domain — xem phần "Rights/License" của từng file.
