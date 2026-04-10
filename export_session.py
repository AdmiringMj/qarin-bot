"""
الخطوة 1: شغّل هذا السكريبت على جهازك لحفظ جلسة تويتر
"""
import asyncio, json
from playwright.async_api import async_playwright

async def export_session():
    print("=" * 50)
    print("🔐 أداة تصدير جلسة تويتر")
    print("=" * 50)
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./twitter_profile",
            headless=False,
            channel="chrome",
            args=["--start-maximized","--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
            viewport=None,
        )
        await context.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"
        )
        page = await context.new_page()
        await page.goto("https://x.com/home", wait_until="domcontentloaded")
        await asyncio.sleep(4)
        if "login" in page.url or "i/flow" in page.url:
            print("🔐 سجّل دخولك في النافذة... (لديك 3 دقائق)")
            await page.wait_for_url("**/home", timeout=180000)
            await asyncio.sleep(3)
        print("✅ مسجّل الدخول! جاري حفظ الجلسة...")
        storage = await context.storage_state()
        with open("twitter_session.json","w") as f:
            json.dump(storage, f)
        print("✅ تم الحفظ في: twitter_session.json")
        print("📤 ارفع هذا الملف مع باقي الملفات على Railway")
        await context.close()

asyncio.run(export_session())
