import csv
from bs4 import BeautifulSoup
from requests import get
from time import sleep

BUY_BOX_FIELDS = ['flex', 'pattern']
FEATURE_FIELDS = ['weight', 'length', 'kick point position']
BASE_RESULT_URL = 'https://www.purehockey.com/c/hockey-sticks-composite-senior'
BATCH_SIZE = 25
BATCH_SLEEP = 300  # 5 minutes


def get_page_soup(url):
    response = get(url)
    page_data = response.text
    return BeautifulSoup(page_data, 'lxml')


def get_buy_box_data(buy_box):
    data = {}
    attribute_categories = buy_box.find_all(class_='attr clearfix')
    for attribute in attribute_categories:
        attribute_name = attribute.find(class_='attr-desc').text.lower()
        if attribute_name and attribute_name in BUY_BOX_FIELDS:
            data[attribute_name] = [item.text for item in attribute.find_all('li')]

    return data


def _remove_flex_suffix(flexes):
    return [flex.replace(' Flex', '') for flex in flexes]


def get_feature_data(table_rows):
    data = {}
    for row in table_rows:
        row_name = row.find(class_='name').text[:-1].lower()
        if row_name and row_name in FEATURE_FIELDS:
            data[row_name] = row.find(class_='value').text

    return data


def get_stick_data_from_page(stick_url):
    soup = get_page_soup(stick_url)

    feature_rows = soup.find(id='features_tab').find_all('tr')
    buy_box = soup.find(class_='buy-box').find(id='attributes')

    stick_data = {'year': soup.find(class_='year-num').text[0:4],
                  'name': soup.find(class_='name item-name').text,
                  'url': stick_url}
    stick_data.update(get_feature_data(feature_rows))
    stick_data.update(get_buy_box_data(buy_box))
    stick_data['flex'] = _remove_flex_suffix(stick_data['flex'])

    return stick_data


def get_num_of_pages():
    base_page_soup = get_page_soup(BASE_RESULT_URL)
    page_selector = base_page_soup.find(class_='pager').find_all('a')
    return page_selector[-2].text


def get_all_stick_urls_for_page(result_page_url):
    result_page = get_page_soup(result_page_url)
    results_grid = result_page.find(id='results-grid').find_all(class_='item')
    stick_urls = []
    for item in results_grid:
        stick_urls.append(item.find(class_='image').a['href'])

    return stick_urls


def get_all_stick_urls(num_of_pages):
    if not num_of_pages.isdigit():
        print('FAILED: Num of pages is not a number!')
        return

    all_stick_urls = []
    for i in range(1, int(num_of_pages)+1):

        result_page_url = BASE_RESULT_URL + f'?pg={i}'
        print('Hitting: ' + result_page_url)
        all_stick_urls.extend(
            get_all_stick_urls_for_page(result_page_url)
        )
        sleep(5)

    return all_stick_urls


def get_all_stick_data(stick_urls):
    stick_data = []

    for stick_url in stick_urls:
        print('Hitting: ' + stick_url)
        try:
            stick_data.append(get_stick_data_from_page(stick_url))
        except Exception as e:
            print(e)
            print('ERROR: FAILED TO GET STICK AT ' + stick_url)
        sleep(5)

    return stick_data


def _split_into_batches(stick_urls):
    return [stick_urls[x:x+BATCH_SIZE] for x in range(0, len(stick_urls), BATCH_SIZE)]


def write_to_csv(stick_data):
    with open('stick_data.csv', mode='w', newline='') as stick_file:
        csv_writer = csv.writer(stick_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(
            ['YEAR', 'NAME', 'FLEX', 'CURVE', 'KICKPOINT', 'WEIGHT', 'LENGTH', 'URL'])
        for data in stick_data:
            csv_writer.writerow([
                data['year'], data['name'], data['flex'],
                data['pattern'], data['kick point position'],
                data['weight'], data['length'], data['url']
            ])


def run_task():
    num_pages = get_num_of_pages()
    stick_urls = get_all_stick_urls(num_pages)
    batched_urls = _split_into_batches(stick_urls)

    all_stick_data = []
    for url_batch in batched_urls:
        all_stick_data.extend(get_all_stick_data(url_batch))
        print('Sleeping between batches so it doesn\'t yell at me.')
        sleep(BATCH_SLEEP)

    print(all_stick_data)
    write_to_csv(all_stick_data)
    return all_stick_data


completed_data = run_task()
print('~~~~~~~~~~~~end~~~~~~~~~~~~~~~~~~')