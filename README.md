# Scrap Amazon with Playwright
This code is a test of the Playwright library. It asynchronously scraps Amazon's website.
## 1) Installation
**- Clone**
```bash
git clone https://github.com/ignacio-nava/simple_playwright_test.git
cd simple_playwright_test
```
**- Create and activate the virtual enviroment**

**- Install requirements**
```bash
pip install -r requirements.txt
```
## 2) Usage
```bash
python main.py
```
## 3) Options

**--semaphore** *SEMAPHORE*, by default: 4 
                       
**--last-pagination** *LAST_PAGINATION*, by default: 4 
                       
**--output-file-name** *OUTPUT_FILE_NAME*, by default: products
                       
Example
```bash
python main.py --semaphore=2 --last-pagination=5 --output-file-name=results
```
