from flask import Flask, request, send_file, render_template
from selenium import webdriver
import os
import time
import glob

app = Flask(__name__)

# Configure the Flask app
app.config['SECRET_KEY'] = 'mysecretkey'

# Define a route for the main page
@app.route('/')
def index():
    # Find the most recent screenshot file
    screenshots = glob.glob('screenshots/screenshot-*.png')
    screenshots.sort(key=os.path.getmtime, reverse=True)
    latest_screenshot = screenshots[0] if screenshots else None

    return render_template('index.html', latest_screenshot=latest_screenshot)

# Define a route for taking a screenshot
@app.route('/screenshot')
def screenshot():
    url = request.args.get('url')
    print('Screenshot requested for URL:', url)
    screenshot_type = request.args.get('screenshot_type')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    if screenshot_type == 'mobile':
        options.add_argument('window-size=375,812')
    else:
        options.add_argument('window-size=1920,1200')
    driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(executable_path='C:\\Users\\eines\\Downloads\\chromedriver_win32\\chromedriver', options=options)
    try:
        driver.get(url)
        count = len(os.listdir('screenshots'))
        screenshot_file = f'screenshots/screenshot-{count}.png'
        driver.save_screenshot(screenshot_file)
        driver.quit()
        print('Screenshot saved to file:', screenshot_file)
        latest_screenshot = os.path.join(os.getcwd(), screenshot_file)
        return send_file(screenshot_file, mimetype='image/png', as_attachment=False, attachment_filename='screenshot.png', cache_timeout=0), latest_screenshot
    except Exception as e:
        print('Error taking screenshot:', str(e))
        driver.quit()
        return 'Error taking screenshot'


if __name__ == '__main__':
    app.run(debug=True)
