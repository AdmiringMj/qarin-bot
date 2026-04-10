"""
🤖 Qaren Cloud Bot - نسخة السيرفر السحابي
يعمل headless على Railway 24/7
"""
import asyncio, json, os, random
from datetime import datetime
from playwright.async_api import async_playwright

KEYWORDS = [
    "تطبيق جاهز",
    "اسعار تطبيقات التوصيل",
    "تطبيق هنقرستيشن",
    "تطبيق كيتا",
    "تطبيق نينجا",
    "سعر الوجبة",
]
BOT_KEYWORDS = [
    "كوبون","كود خصم","كود","خصم","discount","promo","coupon",
    "free delivery","اشترك","تابعنا","فولو","follow","BTY","CUP",
    "CODE","PROMO","%off","تطبيقنا","toyou",
]

APP_LINK = "https://apps.apple.com/sa/app/%D9%82%D8%A7%D8%B1%D9%86-%D9%88%D9%81%D8%B1-%D9%81%D9%84%D9%88%D8%B3%D9%83/id6759526406"

REPLIES = [
    f"تعبت وأنت تقارن بين تطبيقات التوصيل؟ حمّل تطبيق قارن الحين ووفر فلوسك! 😍\n{APP_LINK}",
    f"مو لازم تدور بنفسك! 🎯 تطبيق قارن يقارن لك أسعار كل تطبيقات التوصيل بضغطة واحدة\n{APP_LINK}",
    f"وفّر وقتك وفلوسك مع تطبيق قارن! 💰 يجمع لك كل عروض التوصيل في مكان واحد\n{APP_LINK}",
    f"جرّب تطبيق قارن وشوف الفرق! 🔥 أرخص سعر توصيل بين كل التطبيقات بثانية واحدة\n{APP_LINK}",
    f"ليش تدفع أكثر؟ 🤔 تطبيق قارن يطلعلك أوفر تطبيق توصيل على طلبك بالضبط\n{APP_LINK}",
    f"كل تطبيقات التوصيل في مكان واحد! ✨ حمّل قارن وابدأ توفر من أول طلب\n{APP_LINK}",
    f"رسوم التوصيل وجعتك؟ 😅 تطبيق قارن يلاقيلك الأرخص بين كل التطبيقات\n{APP_LINK}",
    f"قبل ما تطلب شيك الأسعار على قارن! 💡 يوفر لك فلوس من كل طلب\n{APP_LINK}",
]

# ─── 100+ تغريدة ترويجية — كل تغريدة تحتوي رابط التطبيق ────────────────────────
PROMO_TWEETS = [
    f"قارن 🆚 أول تطبيق في السعودية يقارن أسعار الوجبات بين جميع تطبيقات التوصيل!\nوفّر أكثر من كل طلب 💰\n{APP_LINK}",
    f"ليش تدفع أكثر وأنت تقدر توفر؟ 🤑\nتطبيق قارن يقارن لك الأسعار بين جاهز، هنقرستيشن، نينجا، كيتا وغيرها بضغطة واحدة!\n{APP_LINK}",
    f"قبل ما تطلب أكلك، افتح قارن! 📱\nشوف أرخص سعر بين كل تطبيقات التوصيل في ثواني ⚡\n{APP_LINK}",
    f"تطبيق قارن = توفير فعلي 💸\nقارن أسعار وجباتك المفضلة بين جميع التطبيقات واختر الأوفر دائمًا!\n{APP_LINK}",
    f"كل يوم تطلب أكل وكل يوم تدفع أكثر من اللازم؟ 😤\nحمّل قارن الحين وابدأ توفر! 🚀\n{APP_LINK}",
    f"قارن بين 🍔 جاهز | هنقرستيشن | نينجا | كيتا | مرسول\nكلها في مكان واحد مع تطبيق قارن! 🎯\n{APP_LINK}",
    f"ما تحتاج تفتح كل تطبيق وتدور 🙄\nقارن يجيبلك أرخص سعر لأي وجبة فوراً! ⚡\n{APP_LINK}",
    f"وفّر على كل طلب مع تطبيق قارن 💚\nمقارنة فورية للأسعار بين جميع تطبيقات التوصيل في السعودية 🇸🇦\n{APP_LINK}",
    f"تخيل توفر 1000 ريال+ في الشهر من طلبات الأكل؟ 🤯\nمع تطبيق قارن هذا ممكن! ابدأ اليوم 👇\n{APP_LINK}",
    f"اسأل نفسك: هل تدفع السعر الصح؟ 🤔\nتطبيق قارن يضمن لك دائمًا أرخص سعر!\n{APP_LINK}",
    f"عروض يومية رهيبة من تطبيقات التوصيل! 🔥\nاكتشفها كلها في مكان واحد على تطبيق قارن!\n{APP_LINK}",
    f"عروض لحظية 🚨 من جميع تطبيقات التوصيل!\nشوفها على قارن قبل ما تنتهي ⏳\n{APP_LINK}",
    f"كل يوم عروض جديدة من هنقرستيشن، جاهز، نينجا وغيرها 🎉\nقارن يجمعها لك في صفحة واحدة!\n{APP_LINK}",
    f"أفضل عروض اليوم من تطبيقات التوصيل 🔥\nلا تفوّتها! افتح قارن الآن\n{APP_LINK}",
    f"خصومات -91% على بعض الوجبات! 😱\nاكتشف أفضل عروض اليوم على تطبيق قارن!\n{APP_LINK}",
    f"وجبتك المفضلة بسعر أقل اليوم؟ 🍕\nتحقق من عروض قارن اليومية الحين!\n{APP_LINK}",
    f"ما تبي تفوّتك عروض اليوم! ⚡\nافتح قارن وشوف كل خصومات التوصيل دفعة واحدة\n{APP_LINK}",
    f"فعّل تنبيه السعر على وجبتك المفضلة 🔔\nقارن يخبرك فور ما ينخفض السعر!\n{APP_LINK}",
    f"ما تحتاج تراقب الأسعار بنفسك! 😌\nتطبيق قارن يراقب ويرسل لك تنبيه فور انخفاض السعر 🔔\n{APP_LINK}",
    f"حدد السعر اللي تبيه وقارن يرسلك تنبيه لما يوصله 🎯\n{APP_LINK}",
    f"نام مرتاح وقارن يراقب الأسعار لك! 😴\nتنبيه فوري عند انخفاض أي سعر 🔔\n{APP_LINK}",
    f"هل سعر وجبتك ارتفع أو انخفض هالأيام؟ 📊\nتاريخ الأسعار متاح على تطبيق قارن!\n{APP_LINK}",
    f"اعرف متى تطلب للحصول على أفضل سعر! 📈\nتطبيق قارن يعرضلك تاريخ أسعار أي وجبة\n{APP_LINK}",
    f"شاهد كيف تغيرت الأسعار خلال الأشهر الماضية 📉\nواكتشف أفضل وقت للطلب مع قارن!\n{APP_LINK}",
    f"تبحث عن أرخص باقة أكل صحي؟ 🥗\nقارن بين شركات الأكل الصحي واختر الأوفر!\n{APP_LINK}",
    f"قارن بين أسعار شركات الاكل الصحي في السعودية 🥙\nووفّر على نظامك الغذائي مع قارن!\n{APP_LINK}",
    f"نظامك الغذائي ما يجب يكون غالي! 💚\nقارن أسعار شركات الأكل الصحي وابدأ توفر\n{APP_LINK}",
    f"وفّر أكثر من 1000 ريال شهرياً على طلبات الأكل! 💰\nمع تطبيق قارن هذا مو مستحيل 💪\n{APP_LINK}",
    f"حاسب كم تدفع على التوصيل شهرياً؟ 😬\nقارن يساعدك توفر جزء كبير منه!\n{APP_LINK}",
    f"1 ريال فرق في التوصيل = 30 ريال في الشهر 💡\nقارن يلاقيلك الفرق دائمًا!\n{APP_LINK}",
    f"جاهز ولا هنقرستيشن؟ نينجا ولا كيتا؟ 🤷\nما عاد تحتاج تتردد! قارن يطلعلك الجواب فوراً\n{APP_LINK}",
    f"نفس الوجبة، أسعار مختلفة في كل تطبيق! 😲\nقارن يكشفلك الفرق ويوفرلك الأكثر\n{APP_LINK}",
    f"هل تعرف إن نفس البرغر قد يكون بسعرين مختلفين؟ 🍔\nاكتشف الفرق مع تطبيق قارن!\n{APP_LINK}",
    f"6 تطبيقات توصيل، سعر واحد أرخص! ⚡\nقارن يطلعه لك في ثواني!\n{APP_LINK}",
    f"طلبت من ماكدونالدز؟ شيك الأسعار على قارن أولاً! 🍟\nقد تجده أرخص في تطبيق ثاني!\n{APP_LINK}",
    f"احصل على إشعار يومي بأفضل العروض من تطبيقات التوصيل! 📲\nفعّله الآن على قارن!\n{APP_LINK}",
    f"كل صباح، أفضل عروض التوصيل على جوالك! ☀️\nمع تطبيق قارن!\n{APP_LINK}",
    f"احفظ وجباتك المفضلة وتابع أسعارها يومياً! ❤️\nميزة المفضلة في تطبيق قارن!\n{APP_LINK}",
    f"ساهم بتحديث الأسعار وانضم لقائمة أفضل المساهمين! 🏆\nكن جزءاً من مجتمع قارن!\n{APP_LINK}",
    f"التوفير مو حظ، التوفير قرار! 💪\nقرر اليوم تحمّل قارن وتوفر على كل طلب\n{APP_LINK}",
    f"فلوسك تستاهل أكثر من رسوم توصيل غير ضرورية! 💸\nقارن يلاقيلك الأرخص دائمًا\n{APP_LINK}",
    f"الفرق بين الحكيم والمسرف: تطبيق قارن 😄\nحمّله الآن!\n{APP_LINK}",
    f"أكل لذيذ + توفير حقيقي = قارن 🍽️💰\n{APP_LINK}",
    f"صديقك اللي يعرف أرخص مطعم في كل تطبيق 👨‍💻\nهو تطبيق قارن!\n{APP_LINK}",
    f"توصيل بـ 5 ريال ولا توصيل بـ 15 ريال لنفس الوجبة؟ 🤯\nاعرف الفرق مع قارن!\n{APP_LINK}",
    f"٦ تطبيقات توصيل ✅\nمقارنة فورية ✅\nتوفير حقيقي ✅\nكل هذا في قارن!\n{APP_LINK}",
    f"جرب هالحسبة:\nطلبين في اليوم × 5 ريال توفير × 30 يوم = 300 ريال! 💰\nهذا ما يوفره قارن شهرياً!\n{APP_LINK}",
    f"في السعودية 6+ تطبيقات توصيل 📱\nلازم تفتحهم كلهم؟ لا! قارن يكفيك 😎\n{APP_LINK}",
    f"الغداء قرّب! قبل ما تطلب، افتح قارن! 🍽️\nثواني توفر لك ريالات!\n{APP_LINK}",
    f"العشا اليوم من أي تطبيق؟ 🌙\nخلّ قارن يختار الأوفر لك!\n{APP_LINK}",
    f"جوعان وما تدري من وين تطلب؟ 😅\nقارن يحل المشكلة ويوفرلك فلوس!\n{APP_LINK}",
    f"وقت الفطور المميز 🌅\nاطلب من أرخص تطبيق مع قارن وابدأ يومك بتوفير!\n{APP_LINK}",
    f"تطبيق قارن - كل ما تحتاجه لتوفير أكثر:\n🔍 مقارنة فورية للأسعار\n🔔 تنبيهات انخفاض الأسعار\n📊 تاريخ الأسعار\n🔥 أفضل العروض اليومية\n{APP_LINK}",
    f"المميزات:\n✅ قارن أسعار أي وجبة فوراً\n✅ تنبيه عند انخفاض السعر\n✅ تاريخ الأسعار\n✅ عروض يومية حصرية\n✅ قائمة المفضلة\nكلها في تطبيق قارن!\n{APP_LINK}",
    f"قارن، أول تطبيق في السعودية يقارن بين أسعار الوجبات في جميع تطبيقات التوصيل!\nابحث عن أي منتج وقارن أسعاره فوراً 🚀\n{APP_LINK}",
    f"صُنع في السعودية 🇸🇦 لأهل السعودية!\nتطبيق قارن يفهم احتياجاتك ويوفر لك دائمًا\n{APP_LINK}",
    f"للسعوديين اللي يحبون التوفير 💚\nتطبيق قارن هو رفيقك في كل طلبة\n{APP_LINK}",
    f"مو بس تطبيق، هو عادة جديدة! 💡\nكل سعودي حكيم يستخدم قارن قبل ما يطلب\n{APP_LINK}",
    f"قول لصديقك اللي يطلب أكل كل يوم عن تطبيق قارن! 👇\nخليه يوفر معك 😄\n{APP_LINK}",
    f"📲 تطبيق قارن متاح الآن على App Store!\nحمّله مجاناً ووفّر من أول طلب\n{APP_LINK}",
    f"مجاني 100% على App Store 🎉\nحمّل قارن الآن وابدأ توفر!\n{APP_LINK}",
    f"الفرق في رسوم التوصيل بين التطبيقات قد يصل لـ 15+ ريال! 😱\nقارن يلاقيلك الأرخص دائمًا\n{APP_LINK}",
    f"نفس الوجبة، فرق السعر قد يصل 30%! 💸\nلازم تعرف هذا مع تطبيق قارن!\n{APP_LINK}",
    f"قبل قارن: أفتح 5 تطبيقات، أضيّع 10 دقائق 😵\nبعد قارن: ثواني وطلبت بأرخص سعر 😎\n{APP_LINK}",
    f"كنت أدفع 18 ريال توصيل\nاليوم أدفع 8 ريال لنفس المطعم 😱\nالسر: تطبيق قارن!\n{APP_LINK}",
    f"كل يوم كنت أفتح جاهز، هنقرستيشن، نينجا واحد واحد 😩\nاليوم أفتح قارن بس وخلاص! ⚡\n{APP_LINK}",
    f"الجمعة = طلبات كثيرة 🎉\nخليها الجمعة اللي توفر فيها مع تطبيق قارن!\n{APP_LINK}",
    f"ويكند مميز = طلبات مميزة 🥳\nوفّر على كل طلباتك مع قارن!\n{APP_LINK}",
    f"آلاف المستخدمين في السعودية يوفرون يومياً مع قارن! 🌟\nانضم إليهم!\n{APP_LINK}",
    f"بدّل عادتك في الطلب اليوم! 🔄\nقارن = توفير حقيقي في جيبك\n{APP_LINK}",
    f"قارن → طلب → وفّر 💚\n{APP_LINK}",
    f"أرخص سعر توصيل بضغطة واحدة ⚡\nتطبيق قارن\n{APP_LINK}",
    f"وفّر كل يوم مع قارن 💰\n{APP_LINK}",
    f"قارن الأسعار. اختر الأوفر. وفّر أكثر. 🎯\n{APP_LINK}",
    f"طلبات أذكى مع تطبيق قارن! 🧠\n{APP_LINK}",
    f"لا تدفع أكثر من اللازم أبداً! 🙅‍♂️\nتطبيق قارن\n{APP_LINK}",
    f"قارن ووفر فلوسك! 💚\nأفضل قرار تاخذه اليوم\n{APP_LINK}",
    f"مستقبل طلبات الأكل الذكية في السعودية 🇸🇦\nتطبيق قارن!\n{APP_LINK}",
    f"ابدأ رحلتك مع التوفير الذكي اليوم! 🚀\nقارن متاح مجاناً على App Store\n{APP_LINK}",
    f"عروض يومية لحظية! ⚡ لا تفوّت أي خصم\nافتح قارن الآن وشوف العروض\n{APP_LINK}",
    f"وفّر أكثر من 1000 ريال على مشترياتك الشهرية من تطبيقات التوصيل مع تطبيق قارن! 💸\n{APP_LINK}",
    f"شاورما من جاهز بـ 28 ريال\nنفس الشاورما من هنقرستيشن بـ 25 ريال؟ 🤷\nقارن يكشف هالأسرار! 😄\n{APP_LINK}",
    f"ما الفرق بين سعر الوجبة في جاهز ونينجا؟ 🤔\nاعرف الجواب فوراً مع قارن!\n{APP_LINK}",
    f"تطبيق قارن يقارن لك أسعار شركات الأكل الصحي! 🥗\nابحث عن باقتك المثالية بأفضل سعر\n{APP_LINK}",
    f"هل تعلم؟ أسعار نفس الوجبة تختلف بين التطبيقات! 📊\nقارن يكشف لك الأرخص دائماً\n{APP_LINK}",
    f"ما في وجبة تستاهل تدفع عليها أكثر من لازم! 🙅\nقارن يكشفلك الحقيقة\n{APP_LINK}",
    f"اكتشف أفضل وقت لطلب وجبتك المفضلة 📅\nمع تاريخ الأسعار في تطبيق قارن!\n{APP_LINK}",
    f"كل تطبيقات التوصيل في السعودية في مكان واحد! 🇸🇦\nقارن — حمّله مجاناً\n{APP_LINK}",
    f"عروض اليوم من Amazon و تطبيقات التوصيل 🛍️\nكلها في تطبيق قارن!\n{APP_LINK}",
    f"مجتمع قارن يكبر كل يوم! 🌱\nانضم وساهم في مساعدة الجميع على التوفير\n{APP_LINK}",
    f"صحتك + توفيرك = تطبيق قارن! 🏃\nقارن أسعار أفضل شركات الأكل الصحي في مكان واحد\n{APP_LINK}",
    f"المدروسين يستخدمون قارن! 🧠\nلأن ليش تدفع أكثر لما تقدر توفر؟\n{APP_LINK}",
    f"قارن بين أسعار شركات الاكل الصحي! 🥦\nوابدأ نظامك الغذائي بأفضل سعر\n{APP_LINK}",
]

REPLIED_IDS_FILE   = "replied_ids.json"
POSTED_TWEETS_FILE = "posted_tweets.json"
SESSION_FILE       = "twitter_session.json"
MAX_REPLIES        = 1   # رد واحد فقط كل جلسة (كل 4 ساعات)
TWEET_INTERVAL_HRS = 2   # تغريدة ترويجية كل ساعتين
REPLY_INTERVAL_HRS = 4   # رد على تغريدات كل 4 ساعات

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def load_json(path, default):
    return json.load(open(path)) if os.path.exists(path) else default

def save_json(path, data):
    with open(path,"w") as f: json.dump(data, f)

def is_bot(text):
    t = text.lower()
    return any(k.lower() in t for k in BOT_KEYWORDS)

def should_post(last_ts):
    return (datetime.now().timestamp() - last_ts) / 3600 >= TWEET_INTERVAL_HRS

def should_reply(last_ts):
    return (datetime.now().timestamp() - last_ts) / 3600 >= REPLY_INTERVAL_HRS

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
    idx, text = next_tweet(used)
    log(f"📣 نشر تغريدة #{idx+1}/{len(PROMO_TWEETS)}...")
    try:
        await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(3)
        btn = await page.query_selector('[data-testid="SideNav_NewTweet_Button"]')
        if btn:
            await btn.click()
            await asyncio.sleep(2)
        box = await page.query_selector('[data-testid="tweetTextarea_0"]')
        if not box: return used, False
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
        log(f"❌ {e}")
    return used, False

async def run_bot():
    replied      = set(load_json(REPLIED_IDS_FILE, []))
    pt           = load_json(POSTED_TWEETS_FILE, {"last_posted":0,"used":[],"last_replied":0})
    last_ts      = pt.get("last_posted", 0)
    last_replied = pt.get("last_replied", 0)
    used_idx     = set(pt.get("used", []))
    replies_count = 0

    if not os.path.exists(SESSION_FILE):
        log("❌ twitter_session.json غير موجود! شغّل export_session.py أولاً")
        return

    with open(SESSION_FILE) as f:
        session = json.load(f)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu",
                  "--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            storage_state=session,
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width":1280,"height":900},
            locale="ar-SA",
        )
        await context.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"
        )
        page = await context.new_page()

        log("🔍 التحقق من الجلسة...")
        await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)

        if "login" in page.url or "i/flow" in page.url:
            log("❌ الجلسة منتهية! أعد تشغيل export_session.py على جهازك وارفع الملف")
            await browser.close()
            return

        log("✅ الجلسة صالحة!")

        # ── تغريدة ترويجية كل ساعتين ──────────────────────────────────────
        if should_post(last_ts):
            used_idx, posted = await post_tweet(page, used_idx)
            if posted:
                last_ts = datetime.now().timestamp()
        else:
            rem = TWEET_INTERVAL_HRS - (datetime.now().timestamp() - last_ts)/3600
            log(f"⏱️ التغريدة الترويجية القادمة بعد {rem:.1f} ساعة")

        # ── رد على تغريدة واحدة كل 4 ساعات ────────────────────────────────
        if not should_reply(last_replied):
            rem_r = REPLY_INTERVAL_HRS - (datetime.now().timestamp() - last_replied)/3600
            log(f"⏱️ الرد القادم بعد {rem_r:.1f} ساعة")
            save_json(POSTED_TWEETS_FILE, {"last_posted":last_ts,"used":list(used_idx),"last_replied":last_replied})
            await browser.close()
            return

        log("💬 وقت الرد على تغريدة...")
        for kw in KEYWORDS:
            if replies_count >= MAX_REPLIES: break
            log(f"🔍 {kw}")
            url = f"https://x.com/search?q={kw.replace(' ','%20')}&src=typed_query&f=live"
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
            except: continue
            await asyncio.sleep(4)
            tweets = await page.query_selector_all('[data-testid="tweet"]')
            log(f"📬 {len(tweets)} تغريدة")
            for tweet in tweets[:8]:
                if replies_count >= MAX_REPLIES: break
                try:
                    lnk = await tweet.query_selector('a[href*="/status/"]')
                    if not lnk: continue
                    href = await lnk.get_attribute("href")
                    tid = href.split("/status/")[1].split("/")[0].split("?")[0]
                    if tid in replied: continue
                    tel = await tweet.query_selector('[data-testid="tweetText"]')
                    txt = await tel.inner_text() if tel else ""
                    if is_bot(txt) or "apps.apple.com" in txt or "play.google.com" in txt:
                        replied.add(tid); continue
                    log(f"👤 {txt[:60]}...")
                    rbtn = await tweet.query_selector('[data-testid="reply"]')
                    if not rbtn: continue
                    await rbtn.click()
                    await asyncio.sleep(2)
                    rbox = await page.query_selector('[data-testid="tweetTextarea_0"]')
                    if not rbox:
                        await page.keyboard.press("Escape"); continue
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
                        log(f"✅ رد ({replies_count}/{MAX_REPLIES})")
                        await asyncio.sleep(random.randint(25, 50))
                    else:
                        await page.keyboard.press("Escape")
                except Exception as e:
                    log(f"⚠️ {e}")
                    try: await page.keyboard.press("Escape")
                    except: pass
            await asyncio.sleep(5)

        if replies_count > 0:
            last_replied = datetime.now().timestamp()
        save_json(REPLIED_IDS_FILE, list(replied)[-5000:])
        save_json(POSTED_TWEETS_FILE, {"last_posted":last_ts,"used":list(used_idx),"last_replied":last_replied})
        log(f"📊 {replies_count} ردود")
        await browser.close()

async def main():
    log("=" * 55)
    log(f"🤖 قارن Cloud Bot | {len(PROMO_TWEETS)} تغريدة ترويجية كل {TWEET_INTERVAL_HRS}س | رد واحد كل {REPLY_INTERVAL_HRS}س")
    log("=" * 55)
    while True:
        await run_bot()
        log("💤 انتظار ساعة...")
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
