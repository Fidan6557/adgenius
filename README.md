# AdGenius

AI əsaslı multi-platform reklam generatoru. Bir biznes adı və məhsul/xidmət
məlumatından Instagram, Facebook və TikTok üçün platformaya uyğun üç fərqli
reklam mətni yaradır.

**AI / Prompt Engineer Intern — Technical Assignment**

[GitHub repository](https://github.com/Fidan6557/adgenius)

> Railway demo linki deploy tamamlandıqdan sonra buraya əlavə edilməlidir.

## Əsas imkanlar

- Instagram üçün emosional caption və tam 7 uyğun hashtag
- Facebook üçün detallı, axıcı reklam mətni və güclü CTA
- TikTok üçün qısa, diqqətçəkici viral hook
- Üç OpenAI sorğusunun `asyncio.gather` ilə paralel icrası
- Azərbaycan və İngilis interfeys seçimləri
- Nəticələrin bir kliklə kopyalanması
- Eyni məlumatlarla yenidən generasiya
- Son 5 generasiyanın sessiya tarixçəsi
- Responsiv və əlçatan light-theme interfeys
- Input validation və təhlükəsiz DOM rendering
- Railway üçün Docker və health-check konfiqurasiyası

## Texnologiyalar

| Hissə | Texnologiya |
|---|---|
| Backend | Python, FastAPI, Pydantic |
| AI | OpenAI GPT-4o, async Python SDK |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Deployment | Docker, Railway |

## Arxitektura

```text
İstifadəçi
    │
    ▼
Vanilla JS frontend
    │  POST /generate
    ▼
FastAPI + Pydantic validation
    │
    ├── Instagram prompt ─┐
    ├── Facebook prompt ──┼── asyncio.gather ──► OpenAI GPT-4o
    └── TikTok prompt ────┘
    │
    ▼
JSON response → nəticə kartları
```

Platformaların hər biri ayrıca system və user promptundan istifadə edir. Bu,
tonun, uzunluğun, CTA-nın və formatın hər platformanın davranışına uyğun
idarə olunmasına imkan verir.

## Layihə strukturu

```text
ad-generator/
├── main.py
├── prompts.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
├── railway.toml
├── .env.example
├── tests/
│   └── test_app.py
└── templates/
    └── index.html
```

## Lokal quraşdırma

### 1. Repository-ni klonlayın

```bash
git clone https://github.com/Fidan6557/adgenius.git
cd adgenius
```

### 2. Virtual environment yaradın

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Asılılıqları quraşdırın

```bash
pip install -r requirements.txt
```

### 4. Environment dəyişənini əlavə edin

`.env.example` faylını `.env` adı ilə kopyalayın:

```env
OPENAI_API_KEY=sk-your-real-api-key
```

`.env` Git tərəfindən izlənilmir. Real API açarını repository-yə əlavə etməyin.

### 5. Tətbiqi başladın

```bash
uvicorn main:app --reload
```

Brauzerdə açın:

```text
http://127.0.0.1:8000
```

## Testlər

Development asılılıqlarını quraşdırın və testləri başladın:

```bash
pip install -r requirements-dev.txt
pytest -q
```

Test dəsti ana səhifəni, health-check endpoint-ini, input validation-u və üç
OpenAI çağırışının ardıcıl deyil, paralel icra olunduğunu yoxlayır. Testlər real
API açarı və ödənişli OpenAI sorğusu istifadə etmir.

## API istifadəsi

### `POST /generate`

Sorğu:

```json
{
  "business_name": "Luna Coffee",
  "product": "yulaf südlü latte",
  "language": "az"
}
```

Cavab:

```json
{
  "instagram": "...",
  "facebook": "...",
  "tiktok": "..."
}
```

### `GET /health`

Railway deployment health-check üçün:

```json
{
  "status": "ok"
}
```

## Nümunə giriş və çıxışlar

Aşağıdakı nümunələr prompt dizaynının platformalar arasında ton və struktur
fərqini göstərir. Real nəticələr generativ modelə görə dəyişə bilər.

### Nümunə 1 — Luna Coffee

**Giriş**

- Biznes: `Luna Coffee`
- Məhsul/xidmət: `Yulaf südlü latte`

**Instagram**

> Səhərin bir az daha yumşaq başlasa, necə olardı? ☕ Luna Coffee-də yulaf
> südlü latte ilk qurtumdan sakit bir səhər hissi yaradır: məxməri tekstura,
> isti qəhvə ətri və günə tələsmədən başlamaq üçün balaca bir fasilə 🌿✨
> Dostunla söhbətə, kitabınla tək qalmağa və ya sadəcə özünə vaxt ayırmağa
> yaraşan həmin fincan budur 🤍 Bu gün yolunu Luna Coffee-dən sal, bəlkə yeni
> sevimli dadını tapdın.
>
> #YulafSüdlüLatte #QəhvəSevərlər #LunaCoffee #BakıKafeləri #CoffeeTime
> #Lifestyle #GününDadı

**Facebook**

> Bəzən yaxşı bir günün çatışmayan hissəsi sadəcə doğru fincandır.
>
> Yulaf südlü lattenin məxməri teksturası, təzə qəhvənin isti ətri və hər
> qurtumdan sonra qalan yumşaq dad səhərini daha rahat, fasiləni isə daha
> xüsusi edir. Özünə ayırdığın bir neçə dəqiqə günün ən xoş anına çevrilir.
> Luna Coffee qonaqlarının yenidən seçdiyi bu dad artıq bir çox səhərin
> sevimli vərdişidir.
>
> Gəl, öz fincanını kəşf et.

**TikTok**

> Bu latte səhər rutinimi tamamilə dəyişdi

### Nümunə 2 — Narin Studio

**Giriş**

- Biznes: `Narin Studio`
- Məhsul/xidmət: `Əl işi minimalist gümüş boyunbağı`

**Instagram**

> Bəzən bütün görünüşü dəyişən detal ən sakit olanıdır ✨ Narin Studio-nun əl
> işi gümüş boyunbağısı işığı incə şəkildə tutur, sevdiyin köynəyə də, xüsusi
> axşam geyiminə də özünəməxsus zəriflik qatır 🤍 Hər toxunuşunda ustanın
> diqqətini hiss etdiyin bu parça sadəcə aksesuar deyil — gündəlik üslubunun
> kiçik imzasıdır 🌙 Özün üçün seç, ya da dəyər verdiyin birinə mənalı hədiyyə
> et 🎁 Hansı görünüşlə tamamlayacağını təsəvvür et.
>
> #ƏlİşiZinət #GümüşBoyunbağı #NarinStudio #MinimalStil #MadeInAzerbaijan
> #JewelryLover #StyleInspiration

**Facebook**

> Görünüşündə səni ifadə edən o incə detal artıq buradadır.
>
> Dərinin üzərində sərin gümüş toxunuşunu, işıq düşəndə yaranan yumşaq
> parıltını və ən sadə geyimin belə tamamlanmış görünməsini təsəvvür et. Narin
> Studio-nun əl işi boyunbağısı hər gün taxmaq istədiyin, zaman keçdikcə
> hekayənin bir hissəsinə çevrilən parçadır. Zərif və fərqli seçim axtaranların
> diqqəti artıq bu kolleksiyadadır.
>
> Öz detalını bu gün seç.

**TikTok**

> Bunu taxdım, hamı haradan aldığımı soruşdu

### Nümunə 3 — FitBox

**Giriş**

- Biznes: `FitBox`
- Məhsul/xidmət: `Həftəlik sağlam yemək abunəliyi`

**Instagram**

> “Bu gün nə yeyim?” sualı artıq vaxtını almasın 🥗 FitBox həftəlik menyunu
> sənin üçün planlayır: rəngli tərəvəzlər, doyumlu porsiyalar və qapağı açılan
> kimi iştaha gətirən təzə dadlar 🌱 Həm iş günündə enerjini qoruyursan, həm də
> mətbəxdə saatlarla qalmaq əvəzinə özünə vaxt ayırırsan ⏳💚 Növbəti həftəni
> daha rahat yaşamaq istəyirsənsə, menyuya bir göz gəzdir.
>
> #SağlamQidalanma #FitBox #MealPrep #BakıYeməkləri #HealthyLifestyle
> #GündəlikEnerji #FoodInspiration

**Facebook**

> Həftənin daha yüngül keçməsi hazır yeməkdən əvvəl hazır qərarla başlayır.
>
> Soyuducunu açanda səni rəngli, təzə və balanslı yeməklərin qarşıladığını
> təsəvvür et. Vaxtın özünə qalır, gün ərzində enerjin sabit olur və hər
> porsiyada həm doyum, həm də rahatlıq hiss edirsən. FitBox artıq planlı
> qidalanmanı gündəlik həyatına qatan insanların həftəlik seçimidir.
>
> Həftəlik menyunu indi seç.

**TikTok**

> Bu qutular həftəmi gözlənilmədən xilas etdi

## Railway deployment

1. [Railway](https://railway.com/) hesabına daxil olun.
2. **New Project → Deploy from GitHub repo** seçin.
3. `Fidan6557/adgenius` repository-sini seçin.
4. Service-in **Variables** bölməsinə bunu əlavə edin:

   ```text
   OPENAI_API_KEY=sk-your-real-api-key
   ```

5. Deploy-u başladın.
6. **Settings → Networking → Generate Domain** seçərək public URL yaradın.
7. Yaranmış URL-i bu README-nin yuxarısına və intern müraciətinə əlavə edin.

Docker container Railway-in təqdim etdiyi `PORT` dəyişənini avtomatik istifadə
edir. `/health` endpoint-i deployment aktiv edilməzdən əvvəl tətbiqin hazır
olduğunu yoxlamaq üçün konfiqurasiya edilib.

## Təhlükəsizlik

- API açarı yalnız environment dəyişənindən oxunur.
- `.env` faylı `.gitignore` daxilindədir.
- Request body Pydantic ilə yoxlanılır və artıq sahələr qəbul edilmir.
- İstifadəçi məlumatları `textContent` ilə göstərilir; model cavabları HTML
  kimi icra edilmir.
- Frontend tarixçəsi yalnız cari brauzer sessiyasının yaddaşındadır və səhifə
  yeniləndikdə silinir.

## Qiymətləndirmə tələblərinə uyğunluq

- [x] Biznes adı və məhsul/xidmət girişi
- [x] Eyni girişdən üç fərqli platforma çıxışı
- [x] Instagram caption və minimum 5 hashtag
- [x] Facebook detallı reklam mətni və CTA
- [x] TikTok diqqətçəkici hook
- [x] Platformalara uyğun ayrıca prompt dizaynı
- [x] OpenAI API inteqrasiyası
- [x] Oxunaqlı və strukturlaşdırılmış kod
- [x] Responsiv UI/UX
- [x] Bonus funksiyalar: regenerate, copy, dil seçimi və tarixçə
- [x] Docker və Railway hazırlığı
- [x] README-də ən azı 3 giriş–çıxış nümunəsi

## Müəllif

**Fidan**  
AI / Prompt Engineer Intern namizədi
