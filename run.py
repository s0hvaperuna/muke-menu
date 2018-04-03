import os
import subprocess
import shlex


# https://github.com/shawnbutton/PythonHeadlessChrome/blob/master/driver_builder.py
def enable_download_in_headless_chrome(driver, download_dir):
    # add missing support for chrome "send_command"  to selenium webdriver
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)


if __name__ == '__main__':
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    prefs = {'download.default_directory': os.getcwd(),
                 'download.prompt_for_download': False,
                 'download.directory_upgrade': True,
                 'safebrowsing.enabled': False,
                 'safebrowsing.disable_download_protection': True}

    chrome_options.add_experimental_option('prefs', prefs)

    chrome_options.add_argument("--headless")

    driver = Chrome(r'C:\Users\PVUSER\Downloads\chromedriver_win32\chromedriver.exe', options=chrome_options)
    driver.set_window_size(1300, 1800)
    driver.get('http://ruokalistat.leijonacatering.fi/#/05b0c494-f813-e511-892b-78e3b50298fc')
    enable_download_in_headless_chrome(driver, os.getcwd())
    #driver.get_screenshot_as_png()
    while True:
        try:
            driver.execute_script("$('a:contains(\"Varusmiesten ruokalista\")')[0].click()")
        except:
            try:
                driver.execute_script("$('a:contains(\"Varusmiesten ruokalista\")')[0].click()")
            except:
                driver.implicitly_wait(3)
            else:
                break
        else:
            break

    driver.implicitly_wait(20)
    driver.execute_script("document.getElementsByClassName('btn btn-default ng-scope')[0].click()")
    driver.implicitly_wait(30)
    p = os.path.join(os.getcwd(), 'menu_Varusmiesten ruokalista.pdf')
    out = os.path.join(os.getcwd(), 'ruokalista.png')
    args = shlex.split('magick convert -density 300 -quality 1 -depth 8 "{}" "{}"'.format(p, out))
    p = subprocess.call(args)
    driver.close()

    import bot

    gonabot = bot.GonaBot('!')
    gonabot.run('NDI1NzIyMzI5NDExMzU0NjI2.DZLkWA.-O9vRVAxQZMquDjq1ul5vW2w714')
