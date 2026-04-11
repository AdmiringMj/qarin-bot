"""
🤖 Qaren Cloud Bot - نسخة السيرفر السحابي
يعمل headless (بدون نافذة) على Railway 24/7
"""

import asyncio
import json
import os
import random
from datetime import datetime
from playwright.async_api import async_playwright

# ─── الكلمات المفتاحية للبحث ────────────────────────────────────────────────────
KEYWORDS = [
    "تطبيق جاهز",
    "تطبيق هنقرستيشن",
    "تطبيق كيتا",
    "تطبيق توصيل",
    "تطبيق تو يو",
    "تطبيق ذا شيفز",
    "تطبيق مستر مندوب",
    "تطبيق مرسول",
    "اسعار التوصيل",
    "طلبت من مطعم",
    "رسوم التوصيل",
    "توصيل غالي",
    "سعر التوصيل",
    "طلب اكل",
    "اطلب اكل",
]

BOT_KEYWORDS = [
    "كوبون", "كود خصم", "كود", "خصم", "discount", "promo", "coupon",
    "أقوى كوبون", "free delivery", "اشترك", "تابعنا", "فولو", "follow",
    "BTY", "CUP", "CODE", "PROMO", "%off", "تطبيقنا", "toyou",
]

APP_LINK = "https://apps.apple.com/sa/app/%D9%82%D8%A7%D8%B1%D9%86-%D9%88%D9%81%D8%B1-%D9%81%D9%84%D9%88%D8%B3%D9%83/id6759526406"

# ─── الردود ────────────────────────────────────────────────────────────────────
REPLIES = [
    f"تعبت وأنت تقارن بين تطبيقات التوصيل؟ 😅\nحمّل تطبيق قارن الحين ووفر فلوسك بضغطة واحدة!\nنفس الوجبة، أرخص سعر، بدون تعب 💰\n{APP_LINK}",
    f"مو لازم تدور بنفسك! 🎯\nتطبيق قارن يقارن لك أسعار جاهز، هنقرستيشن، نينجا، كيتا وكل التطبيقات دفعة وحدة!\nابدأ توفر من أول طلب 👇\n{APP_LINK}",
    f"وفّر وقتك وفلوسك مع تطبيق قارن! 💸\nبدل ما تفتح 5 تطبيقات، افتح واحد يجمعهم كلهم!\nوفّر ريالات على كل طلب بدون أي جهد ✨\n{APP_LINK}",
    f"جرّب تطبيق قارن وشوف الفرق بنفسك! 🔥\nفي ثواني يطلعلك أرخص سعر توصيل بين كل التطبيقات\nالتوفير الحقيقي يبدأ من هنا 💪\n{APP_LINK}",
    f"ليش تدفع أكثر وأنت ما تدري؟ 🤔\nتطبيق قارن يكشفلك الفرق الحقيقي بين الأسعار ويوفرلك الفلوس اللي تستاهلها!\nجرّبه مجاناً الآن 🎉\n{APP_LINK}",
    f"كل تطبيقات التوصيل في مكان واحد! ✨\nقارن الأسعار، شوف العروض، اختار الأوفر\nكل هذا مجاني 100% على App Store!\n{APP_LINK}",
    f"رسوم التوصيل وجعتك؟ 😤\nتطبيق قارن يلاقيلك الأرخص بين كل التطبيقات في ثواني!\nما رح تصدق كم كنت تدفع زيادة قبله 😱\n{APP_LINK}",
    f"قبل ما تطلب أكلك القادم، افتح قارن! 💡\nيقارن لك الأسعار من جاهز لهنقرستيشن لنينجا وغيرها\nويوفرلك فلوس حقيقية من كل طلب 💰\n{APP_LINK}",
]

# ─── التغريدات الترويجية مع الصور ──────────────────────────────────────────────
# كل تغريدة مرتبطة بصورة معينة من مجلد images/
PROMO_TWEETS = [
    {
        "text": f"💸 نفس الوجبة، فروق أسعار مو طبيعية بين التطبيقات!\n\nشفت الفرق؟ حتى 46% فرق على نفس الطلب! 😱\nتطبيق قارن يكشفلك هالفروق ويوفرلك الأكثر تلقائياً\n\nحمّله مجاناً الآن 👇\n{APP_LINK}",
        "image": "images/price_diff.jpg"
    },
    {
        "text": f"🏆 مقارنة فورية بين كل تطبيقات التوصيل!\n\nمن الأرخص لأغلى بضغطة واحدة:\n✅ نينجا | تو يو | جاهز | هنقرستيشن | ذا شيفز\n\nما تحتاج تفتح كل تطبيق بنفسك، قارن يسوّيها عنك ⚡\n{APP_LINK}",
        "image": "images/price_compare1.jpg"
    },
    {
        "text": f"📊 اليوم جاهز الأرخص، بكرة قد يتغير!\n\nتطبيق قارن يتابع الأسعار لك يومياً ويرسلك تنبيه فور ما ينخفض سعر وجبتك المفضلة 🔔\n\nفعّل التنبيهات الآن!\n{APP_LINK}",
        "image": "images/price_compare2.jpg"
    },
    {
        "text": f"🔥 أفضل العروض اليومية من تطبيقات التوصيل!\n\nكل يوم عروض حصرية تصل لـ 34% خصم على وجباتك المفضلة\nشوفها كلها في مكان واحد على تطبيق قارن!\n\nلا تفوّت أي صفقة 👇\n{APP_LINK}",
        "image": "images/daily_offers.jpg"
    },
    {
        "text": f"🥗 تبحث عن أرخص باقة أكل صحي؟\n\nقارن بين شريد ميلز، ديلي ميلز وغيرها\nالسعر، عدد الوجبات، ونوع الخطة، كل شيء في مقارنة واحدة!\n\nاختر الأوفر مع تطبيق قارن 💚\n{APP_LINK}",
        "image": "images/healthy_subs.jpg"
    },
    {
        "text": f"قارن 🆚 أول تطبيق في السعودية يقارن أسعار الوجبات بين جميع تطبيقات التوصيل!\n\n🔍 مقارنة فورية للأسعار\n🔔 تنبيهات انخفاض الأسعار\n📊 تاريخ الأسعار\n🔥 أفضل العروض اليومية\n\nوفّر أكثر من كل طلب 💰\n{APP_LINK}",
        "image": "images/price_diff.jpg"
    },
    {
        "text": f"ليش تدفع أكثر وأنت تقدر توفر؟ 🤑\n\nتطبيق قارن يقارن لك الأسعار بين:\nجاهز | هنقرستيشن | نينجا | كيتا | تو يو | مرسول\n\nكلها بضغطة واحدة، وفّر ريالاتك من اليوم! 💪\n{APP_LINK}",
        "image": "images/price_compare1.jpg"
    },
    {
        "text": f"قبل قارن: أفتح 5 تطبيقات وأضيّع 10 دقائق 😵\nبعد قارن: ثواني وطلبت بأرخص سعر 😎\n\nالفرق واضح! جرّبه بنفسك مجاناً\nمتاح على App Store 🇸🇦\n{APP_LINK}",
        "image": "images/price_compare2.jpg"
    },
    {
        "text": f"تخيل توفر مئات الريالات شهرياً من طلبات الأكل! 🤯\n\nطلبين في اليوم × 5 ريال توفير × 30 يوم = 300 ريال!\nهذا ما يوفره تطبيق قارن فعلياً كل شهر 💰\n\nابدأ اليوم!\n{APP_LINK}",
        "image": "images/daily_offers.jpg"
    },
    {
        "text": f"نفس الوجبة، أسعار مختلفة في كل تطبيق! 😲\n\nتطبيق قارن يكشفلك الفرق الحقيقي ويوفرلك الأكثر على كل طلب\n\nصُنع في السعودية 🇸🇦 لأهل السعودية!\nمجاني 100% على App Store 🎉\n{APP_LINK}",
        "image": "images/price_diff.jpg"
    },
    {
        "text": f"احفظ وجباتك المفضلة وتابع أسعارها يومياً! ❤️\n\nميزة المفضلة في تطبيق قارن تخليك دايم على دراية بأحسن وقت للطلب\nما راح تدفع زيادة مرة ثانية! 💸\n{APP_LINK}",
        "image": "images/price_compare1.jpg"
    },
    {
        "text": f"عروض لحظية 🚨 من جميع تطبيقات التوصيل!\n\nشوفها كلها على قارن قبل ما تنتهي ⏳\nتنبيهات فورية + مقارنة أسعار + تاريخ العروض\n\nكل هذا مجاناً في تطبيق قارن! 🔥\n{APP_LINK}",
        "image": "images/daily_offers.jpg"
    },
]

REPLIED_IDS_FILE    = "replied_ids.json"
POSTED_TWEETS_FILE  = "posted_tweets.json"
SESSION_FILE        = "twitter_session.json"
MAX_REPLIES_PER_RUN = 10
TWEET_INTERVAL_HRS  = 1


def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)


def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


def is_bot_tweet(text):
    t = text.lower()
    return any(kw.lower() in t for kw in BOT_KEYWORDS)


def should_post(last_ts):
    return (datetime.now().timestamp() - last_ts) / 3600 >= TWEET_INTERVAL_HRS


def next_tweet(used):
    available = [i for i in range(len(PROMO_TWEETS)) if i not in used]
    if not available:
        used.clear()
        available = list(range(len(PROMO_TWEETS)))
    idx = random.choice(available)
    return idx, PROMO_TWEETS[idx]


async def hd(a=800, b=2000):
    await asyncio.sleep(random.uniform(a/1000, b/1000))


async def post_tweet(page, used):
    idx, tweet_data = next_tweet(used)
    text = tweet_data["text"]
    image_path = tweet_data.get("image", "")

    log(f"📣 نشر تغريدة #{idx+1}...")
    try:
        await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(3)

        btn = await page.query_selector('[data-testid="SideNav_NewTweet_Button"]')
        if btn:
            await btn.click()
            await asyncio.sleep(2)

        box = await page.query_selector('[data-testid="tweetTextarea_0"]')
        if not box:
            return used, False

        # ─── رفع الصورة إن وُجدت ──────────────────────────────────────────────
        if image_path and os.path.exists(image_path):
            try:
                file_input = await page.query_selector('input[data-testid="fileInput"]')
                if not file_input:
                    # جرّب طريقة بديلة
                    file_input = await page.query_selector('input[accept*="image"]')
                if file_input:
                    await file_input.set_input_files(image_path)
                    log(f"🖼️ تم رفع الصورة: {image_path}")
                    await asyncio.sleep(3)  # انتظر اكتمال الرفع
                else:
                    log(f"⚠️ لم يتم العثور على حقل رفع الصورة")
            except Exception as e:
                log(f"⚠️ خطأ في رفع الصورة: {e}")
        elif image_path:
            log(f"⚠️ الصورة غير موجودة: {image_path}")

        # ─── كتابة النص ───────────────────────────────────────────────────────
        await box.click()
        await hd(400, 800)
        await box.type(text, delay=25)
        await hd(1500, 2500)

        send = await page.query_selector('[data-testid="tweetButton"]')
        if send:
            await send.click()
            await asyncio.sleep(3)
            used.add(idx)
            log(f"✅ تم النشر: {text[:60]}...")
            return used, True
    except Exception as e:
        log(f"❌ خطأ في النشر: {e}")
    return used, False


async def run_bot():
    replied  = set(load_json(REPLIED_IDS_FILE, []))
    pt_data  = load_json(POSTED_TWEETS_FILE, {"last_posted": 0, "used": []})
    last_ts  = pt_data.get("last_posted", 0)
    used_idx = set(pt_data.get("used", []))
    replies_count = 0

    if not os.path.exists(SESSION_FILE):
        log("❌ ملف twitter_session.json غير موجود! شغّل export_session.py أولاً")
        return

    with open(SESSION_FILE) as f:
        session = json.load(f)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
                  "--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            storage_state=session,
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
            locale="ar-SA",
        )
        await context.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"
        )
        page = await context.new_page()

        # تحقق تسجيل الدخول
        log("🔍 التحقق من الجلسة...")
        await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)

        if "login" in page.url or "i/flow" in page.url:
            log("❌ الجلسة منتهية! أعد تشغيل export_session.py على جهازك")
            await browser.close()
            return

        log("✅ الجلسة صالحة!")

        # نشر تغريدة ترويجية
        if should_post(last_ts):
            used_idx, posted = await post_tweet(page, used_idx)
            if posted:
                last_ts = datetime.now().timestamp()
            save_json(POSTED_TWEETS_FILE, {"last_posted": last_ts, "used": list(used_idx)})
        else:
            rem = TWEET_INTERVAL_HRS - (datetime.now().timestamp() - last_ts) / 3600
            log(f"⏱️ التغريدة القادمة بعد {rem:.1f} ساعة")

        # البحث والرد
        for kw in KEYWORDS:
            if replies_count >= MAX_REPLIES_PER_RUN:
                break
            log(f"🔍 {kw}")
            url = f"https://x.com/search?q={kw.replace(' ','%20')}&src=typed_query&f=live"
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
            except:
                continue
            await asyncio.sleep(4)

            tweets = await page.query_selector_all('[data-testid="tweet"]')
            log(f"📬 {len(tweets)} تغريدة")

            for tweet in tweets[:8]:
                if replies_count >= MAX_REPLIES_PER_RUN:
                    break
                try:
                    lnk = await tweet.query_selector('a[href*="/status/"]')
                    if not lnk:
                        continue
                    href = await lnk.get_attribute("href")
                    tid = href.split("/status/")[1].split("/")[0].split("?")[0]
                    if tid in replied:
                        continue

                    tel = await tweet.query_selector('[data-testid="tweetText"]')
                    txt = await tel.inner_text() if tel else ""

                    if is_bot_tweet(txt) or "apps.apple.com" in txt or "play.google.com" in txt:
                        replied.add(tid)
                        continue

                    log(f"👤 {txt[:60]}...")
                    rbtn = await tweet.query_selector('[data-testid="reply"]')
                    if not rbtn:
                        continue
                    await rbtn.click()
                    await asyncio.sleep(2)

                    rbox = await page.query_selector('[data-testid="tweetTextarea_0"]')
                    if not rbox:
                        await page.keyboard.press("Escape")
                        continue

                    rt = random.choice(REPLIES)
                    await rbox.click()
                    await hd(400, 800)
                    await rbox.type(rt, delay=40)
                    await hd(1000, 2000)

                    sbtn = await page.query_selector('[data-testid="tweetButton"]')
                    if sbtn:
                        await sbtn.click()
                        await asyncio.sleep(3)
                        replied.add(tid)
                        replies_count += 1
                        log(f"✅ رد ({replies_count}/{MAX_REPLIES_PER_RUN})")
                        await asyncio.sleep(random.randint(25, 50))
                    else:
                        await page.keyboard.press("Escape")
                except Exception as e:
                    log(f"⚠️ {e}")
                    try:
                        await page.keyboard.press("Escape")
                    except:
                        pass
            await asyncio.sleep(5)

        save_json(REPLIED_IDS_FILE, list(replied)[-5000:])
        log(f"📊 {replies_count} ردود")
        await browser.close()


async def main():
    log("=" * 55)
    log("🤖 قارن Cloud Bot — يعمل 24/7 ☁️")
    log("=" * 55)
    while True:
        await run_bot()
        log("💤 انتظار ساعة...")
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
