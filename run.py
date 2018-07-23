import json
import os
import shlex
import traceback
import subprocess

if not os.path.exists('config.json'):
    config = {"chromedriver": "chromedriver",
              "token": None}
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

else:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)


menu_names = ['varusmiesten ruokalista', 'varusmiesruokalista', 'varusmiesateria', 'varusmieslista']


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
    chrome_options.add_argument('--disable-gpu')
    binary = config.get('chrome_binary', None)
    if binary:
        chrome_options.binary_location = binary

    driver = Chrome(config['chromedriver'], options=chrome_options)
    driver.set_window_size(1300, 1800)
    driver.get('http://ruokalistat.leijonacatering.fi/#/05b0c494-f813-e511-892b-78e3b50298fc')
    enable_download_in_headless_chrome(driver, os.getcwd())
    driver.get_screenshot_as_png()  # idk this increase the success rate of the script
    found = False
    i = 0
    driver.execute_script("""jQuery.expr[':'].icontains = function(a, i, m) {
                                return jQuery(a).text().toLowerCase()
                                    .indexOf(m[3].toLowerCase()) >= 0;""") # Case insensitive contains
    while not found and i < 5:
        driver.implicitly_wait(3)
        for name in menu_names:
            try:
                print(f'clicking name {name}')
                driver.execute_script(f"$('a:icontains(\"{name}\")')[0].click()")
            except:
                traceback.print_exc()
                print('Not found')
                pass
            else:
                print('Found')
                found = True
                break
        i += 1

    if not found:
        driver.quit()
        raise TimeoutError('Could not find list in time')

    driver.implicitly_wait(20)
    driver.execute_script("document.getElementsByClassName('btn btn-default ng-scope')[0].click()")
    driver.implicitly_wait(30)
    path = os.path.join(os.getcwd(), f'menu_{name}.pdf')
    out = os.path.join(os.getcwd(), 'ruokalista.png')
    print(f'Converting {path} to {out}')
    args = shlex.split('magick convert -density 300 -quality 1 -depth 8 "{}" "{}"'.format(path, out))
    p = subprocess.call(args)
    print('Converted')
    driver.quit()

    try:
        os.remove(path)
    except OSError:
        pass

    import bot
    print('Starting bot')
    gonabot = bot.GonaBot('!')
    gonabot.run(config['token'])
