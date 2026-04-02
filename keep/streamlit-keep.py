from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

def setup_driver(self):
    logger.info("⚙️ 正在初始化浏览器配置...")
    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'

    # GitHub Actions 无头模式
    if os.getenv('GITHUB_ACTIONS'):
        chrome_options.add_argument('--headless=new')        # 推荐使用 new headless
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')

    # 通用反检测
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    try:
        # 关键修改：让 webdriver-manager 自动下载匹配的 ChromeDriver
        service = ChromeService(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 隐藏 webdriver 属性
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("✅ 浏览器驱动就绪（自动匹配版本）")
    except Exception as e:
        logger.error(f"❌ 驱动初始化失败: {str(e)}")
        raise
