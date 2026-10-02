# API miễn phí / có free tier để làm video

Lọc từ [public-apis/public-apis](https://github.com/public-apis/public-apis), sắp theo từng bước làm video.
Cột **Key**: `Không` = gọi thẳng, không cần đăng ký; `apiKey`/`OAuth` = cần đăng ký lấy key.

## 1. Ảnh & video stock (B-roll, hình nền)

| API | Dùng để | Key | Link |
|---|---|---|---|
| Pexels | Ảnh + **video** stock miễn phí, dùng thương mại được | apiKey | https://www.pexels.com/api/ |
| Pixabay | Ảnh, video, minh hoạ miễn phí | apiKey | https://pixabay.com/api/docs/ |
| Unsplash | Ảnh chất lượng cao | OAuth | https://unsplash.com/developers |
| Lorem Picsum | Ảnh ngẫu nhiên (từ Unsplash), test nhanh | Không | https://picsum.photos/ |
| Lightdrift | Tìm 1,85 triệu ảnh giấy phép mở, kèm thông tin ghi nguồn | apiKey | https://docs.lightdrift.ai |
| Giphy | GIF, sticker | apiKey | https://developers.giphy.com/docs/ |
| Wallhaven | Hình nền độ phân giải cao | apiKey | https://wallhaven.cc/help/api |
| NASA | Ảnh vũ trụ (public domain) | Không (DEMO_KEY) | https://api.nasa.gov |

## 2. Tư liệu lịch sử / bảo tàng (hợp kênh "vi lịch sử")

| API | Dùng để | Key | Link |
|---|---|---|---|
| Wikipedia | Tra cứu nội dung, tóm tắt bài viết | Không | https://www.mediawiki.org/wiki/API:Main_page |
| Wikidata | Dữ kiện có cấu trúc (năm sinh, phát minh…) | Không (đọc) | https://www.wikidata.org/w/api.php?action=help |
| Archive.org | Phim, ảnh, sách, âm thanh cũ (nhiều cái public domain) | Không | https://archive.readme.io/docs |
| Chronicling America | Báo Mỹ cổ (Library of Congress) — ảnh trang báo gốc | Không | https://chroniclingamerica.loc.gov/about/api/ |
| Metropolitan Museum of Art | Ảnh hiện vật, nhiều ảnh CC0 | Không | https://metmuseum.github.io/ |
| Art Institute of Chicago | Tranh, hiện vật | Không | https://api.artic.edu/docs/ |
| Smithsonian Open Access | Hàng triệu ảnh CC0 | apiKey | https://github.com/Smithsonian/smithsonian-openaccess |
| Europeana | Tư liệu bảo tàng châu Âu | apiKey | https://pro.europeana.eu/resources/apis/search |
| Rijksmuseum | Tranh Hà Lan độ phân giải cao | apiKey | https://data.rijksmuseum.nl/object-metadata/api/ |
| Random Useless Facts / Fun Fact | Lấy ý tưởng chủ đề "sự thật thú vị" | Không | https://uselessfacts.jsph.pl/ · https://api.aakhilv.me |

## 3. Nhạc nền & hiệu ứng âm thanh

| API | Dùng để | Key | Link |
|---|---|---|---|
| Freesound | Hiệu ứng âm thanh (SFX), kiểm tra giấy phép từng file | apiKey | https://freesound.org/docs/api/ |
| Jamendo | Nhạc Creative Commons | OAuth | https://developer.jamendo.com/v3.0/docs |
| Sunor | Tạo nhạc AI qua Suno (trả theo credit) | apiKey | https://docs.sunor.cc |
| Lyrics.ovh | Lấy lời bài hát | Không | https://lyricsovh.docs.apiary.io |
| Genius / Musixmatch | Lời + thông tin bài hát | OAuth / apiKey | https://docs.genius.com/ |

## 4. Giọng đọc (TTS) & phụ đề

| API | Dùng để | Key | Link |
|---|---|---|---|
| IBM Text to Speech | Chuyển văn bản thành giọng nói (có free tier) | apiKey | https://cloud.ibm.com/docs/text-to-speech/getting-started.html |
| Audexum | TTS 43 giọng / 32 ngôn ngữ + nhận dạng giọng nói | apiKey | https://audexum.com/docs |
| OpenSubtitles | Tìm/tải phụ đề | apiKey | https://www.opensubtitles.com/ |
| VidWords / TubeToTranscript | Lấy transcript YouTube (SRT, VTT, TXT) để nghiên cứu đối thủ | apiKey | https://vidwords.com/api-docs |

## 5. Dựng / render video tự động bằng code

| API | Dùng để | Key | Link |
|---|---|---|---|
| Shotstack | Dựng video bằng JSON (timeline, chữ, nhạc, chuyển cảnh) | apiKey | https://shotstack.io/ |
| JSON2Video | Slideshow, voice-over, chữ động, watermark | apiKey | https://json2video.com |
| KinoPipe | Các thao tác dựng video cho automation | apiKey | https://kinopipe.com/docs |
| Rendobar | Transcode, gắn phụ đề, watermark | apiKey | https://rendobar.com |
| Duply | Tạo/sửa ảnh và video hàng loạt từ template | apiKey | https://duply.co/docs |

## 6. Thumbnail & xử lý ảnh

| API | Dùng để | Key | Link |
|---|---|---|---|
| Remove.bg / PhotoRoom | Xoá nền ảnh cho thumbnail | apiKey | https://www.remove.bg/api |
| UpRes | Upscale ảnh cũ/mờ lên 4K–8K | apiKey | https://upres.ai/docs/api |
| Kavel | Tạo/sửa ảnh AI, không cần key | Không | https://kavel.readthedocs.io/ |
| Colormind / The Color API | Gợi ý bảng màu | Không | http://colormind.io/api-access/ |

## 7. Đăng tải & phân tích

| API | Dùng để | Key | Link |
|---|---|---|---|
| YouTube Data API | Upload, sửa tiêu đề/mô tả, xem số liệu | OAuth | https://developers.google.com/youtube/ |
| Vimeo / Dailymotion | Đăng lên nền tảng khác | OAuth | https://developer.vimeo.com/ |

---

**Lưu ý bản quyền:** stock (Pexels, Pixabay) và ảnh CC0 (Met, Smithsonian, NASA) thường dùng thương mại được.
Freesound, Jamendo, Archive.org thì **phải xem giấy phép của từng file** (CC-BY bắt buộc ghi nguồn, CC-NC không được kiếm tiền).
Các API phim/truyền hình (TMDb, OMDb…) chỉ cho thông tin/poster, không cho phép dùng cảnh phim.
