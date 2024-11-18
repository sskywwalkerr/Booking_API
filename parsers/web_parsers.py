import requests
import json


def get_data(url=None):
    cookies = {
        'MVID_NEW_LK_OTP_TIMER': 'true',
        'MVID_CHAT_VERSION': '6.6.0',
        'SENTRY_TRANSACTIONS_RATE': '0.1',
        'SENTRY_REPLAYS_SESSIONS_RATE': '0.01',
        'SENTRY_REPLAYS_ERRORS_RATE': '0.01',
        'SENTRY_ERRORS_RATE': '0.1',
        'MVID_FILTER_CODES': 'true',
        'MVID_FLOCKTORY_ON': 'true',
        'MVID_CRITICAL_GTM_INIT_DELAY': '3000',
        'MVID_SP': 'true',
        'MVID_SERVICE_AVLB': 'true',
        'MVID_DIGINETICA_ENABLED': 'true',
        'MVID_IMG_RESIZE': 'true',
        '_userGUID': '0:m0s4xhdq:5Msk~BtLU9GHC4L329vryg0DQ3aSKxo6',
        'mindboxDeviceUUID': 'ec4c7358-34bb-40eb-b1cf-ddc0db0ee6e3',
        'directCrm-session': '%7B%22deviceGuid%22%3A%22ec4c7358-34bb-40eb-b1cf-ddc0db0ee6e3%22%7D',
        '_ym_uid': '1725712944652720966',
        '_ym_d': '1725712944',
        '_ga': 'GA1.1.944521086.1725712944',
        'gdeslon.ru.__arc_domain': 'gdeslon.ru',
        'gdeslon.ru.user_id': 'bc831f30-a741-421b-879b-572c0674c1d2',
        'tmr_lvid': 'b3591a590192a80d45d5868a59b760ef',
        'tmr_lvidTS': '1725712947270',
        'uxs_uid': 'a394f0d0-6d16-11ef-a4c1-93a478a88c01',
        'flocktory-uuid': 'f68e72bf-3afb-4b95-841e-a0e55a2a85a5-1',
        'afUserId': '84840a32-2db6-4690-b872-b27f3f134848-p',
        'MVID_REGION_ID': '5',
        'MVID_CITY_ID': 'CityCZ_2030',
        'MVID_TIMEZONE_OFFSET': '5',
        'MVID_KLADR_ID': '6600000100000',
        'MVID_REGION_SHOP': 'S953',
        'utm_term': '---autotargeting',
        'adid': '172733893065133',
        'MVID_IS_NEW_BR_WIDGET': 'true',
        'MVID_SERVICES': '111',
        'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
        'MVID_GTM_ENABLED': '011',
        'MVID_WEB_SBP': 'true',
        'MVID_CREDIT_SERVICES': 'true',
        'MVID_TYP_CHAT': 'true',
        'MVID_CREDIT_DIGITAL': 'true',
        'MVID_CASCADE_CMN': 'true',
        'MVID_EMPLOYEE_DISCOUNT': 'true',
        'MVID_AB_UPSALE': 'true',
        'MVID_AB_PERSONAL_RECOMMENDS': 'true',
        'MVID_ACCESSORIES_PDP_BY_RANK': 'true',
        'MVID_NEW_CHAT_PDP': 'true',
        'MVID_GROUP_BY_QUALITY': 'true',
        'MVID_DISPLAY_ACCRUED_BR': 'true',
        'MVID_DISPLAY_PERS_DISCOUNT': 'true',
        'MVID_AB_PERSONAL_RECOMMENDS_SRP': 'true',
        'MVID_ACCESSORIES_ORDER_SET_VERSION': '2',
        'MVID_MCOMBO_HISTORY': 'true',
        'MVID_CART_ACCESSORIES_MSERCH_V3': 'true',
        'MVID_MEDIA_STORIES': 'true',
        'MVID_DISABLEDITEM_PRICE': '1',
        'MVID_SRP_SEARCH_V3': 'true',
        'MVID_RECOMENDATION_SET_ALGORITHM': '0',
        'customer_email': 'null',
        'adrcid': 'ASx-3TG3Q5_eFLnSo8q4itA',
        'adrcid': 'ASx-3TG3Q5_eFLnSo8q4itA',
        '__lhash_': '7abac222d56e9edf62601f2e30471e53',
        'MVID_MCOMBO_SUBSCRIPTION': 'true',
        'MVID_WEB_QR': 'true',
        'MVID_CASCADE_EMP_DIS': 'true',
        'MVID_CASCADE_CMN_BR': 'true',
        'MVID_PDP_BUNDLES_MSERCH_V3': 'true',
        'admitad_uid': '---autotargeting',
        '__cpatrack': 'yandex_cpc',
        '__sourceid': 'yandex',
        '__allsource': 'yandex',
        'advcake_track_id': '79490680-aabe-a437-6b2f-3f78a099796c',
        'advcake_session_id': '1cec1b69-9495-fee1-2512-4d71c5681671',
        'advcake_utm_partner': 'cn%3Amg_epk_katalog_p_rf%7Ccid%3A113025235',
        'advcake_utm_webmaster': 'ph%3A52609474065%7Cre%3A52609474065%7Ccid%3A113025235%7Cgid%3A5474475908%7Caid%3A1848619957173588719%7Cadp%3Ano%7Cpos%3Apremium3%7Csrc%3Asearch_none%7Cdvc%3Adesktop%7Ccoef_goal%3A0%7Cregion%3A54%7C%25D0%2595%25D0%25BA%25D0%25B0%25D1%2582%25D0%25B5%25D1%2580%25D0%25B8%25D0%25BD%25D0%25B1%25D1%2583%25D1%2580%25D0%25B3',
        'advcake_click_id': '',
        'AF_SYNC': '1731756044334',
        '__hash_': '2979db5b69349a24b78add55f955a79b',
        'MVID_ENVCLOUD': 'prod2',
        'MVID_GEOLOCATION_NEEDED': 'false',
        '_sp_ses.d61c': '*',
        'dSesn': '05450c88-e48b-feb6-fef9-407978fb8acd',
        '_dvs': '0:m3mz4cdm:27toiw7dJLdoC~3su9tkitNr3Vj3th7Q',
        '_ym_isad': '2',
        '_ym_visorc': 'w',
        '__SourceTracker': 'yandex.ru__organic',
        'admitad_deduplication_cookie': 'yandex.ru__organic',
        'SMSError': '',
        'authError': '',
        'acs_3': '%7B%22hash%22%3A%22768a608b20ce960ff29026da95a81203ec583ad1%22%2C%22nextSyncTime%22%3A1732017606255%2C%22syncLog%22%3A%7B%22224%22%3A1731931206255%2C%221228%22%3A1731931206255%2C%221230%22%3A1731931206255%7D%7D',
        'acs_3': '%7B%22hash%22%3A%22768a608b20ce960ff29026da95a81203ec583ad1%22%2C%22nextSyncTime%22%3A1732017606255%2C%22syncLog%22%3A%7B%22224%22%3A1731931206255%2C%221228%22%3A1731931206255%2C%221230%22%3A1731931206255%7D%7D',
        'adrdel': '1731931206409',
        'adrdel': '1731931206409',
        'domain_sid': 'wXe8SzgkTS5JGKK-vClMg%3A1731931208065',
        'digi_uc': '|v:172733:30064275!173062:30065241:30065299|c:173175:30073620!173193:400302089',
        'advcake_track_url': '%3D20241118QVHjB3bc2GTyGpfTeqRHR997YiAY7zZVdBqt8M2AsbYOdRmRpJFdSmtpmh7xi2gNx8T3PjjmDvAT5cyurf%2BFzap8tqLN%2BIlGIpMdqjF9oo3%2Fp270mq1Yd43pRRAmunBXQmxTh0JipUSYZ1QIK8kzmz2hMDPlZij1GgwFpr%2FtGHxbSRqyK7cFlvmLNbJ9wdkTrVYIyV84p5GUbLJNSD6Tmx29z6RemWef7qbQr0WjVdk3GEU1hBBJASjF0gA5av6JIdcOw4EwanfdSp6FTSLq3vFPs8d8csphERiVH6XgilslvDtyFX4g5iBq07rULKTT1CxWzNXDCedlG1sFHTwzGhL59SwM1iqAlzyjmYatFblk0gW0mnEDdhHwzMNYh7qo%2F3eVToZRqVngkuItRbz6onxfZDMp32J4A2zJ%2FIctKNB%2FFOBP2NemDYczYL68HJ6UKQmU3baK13CohhyOFQxHVrtST%2BJAvN5mKrIzSrdREsJx85hptbJEUsZIAi76%2BVV1553p22tSKwmF0D0he0FgkpvvG0C7Lf%2FpNPdCXbWiJSLQdlYiBHQMDr1evO36domcSveODmixQSYY92NxOVzDazbxI7h2%2FCuXXCgKjvEe5HEy92dWHLRohgPW3jI6jnwnyH6%2FL6GZ2WUDEeAJBAu8ZZ9OfJ3v4ulzQ5zZj8BPIX5rqJgVTywkY2ECqud2IwUE%2BbTIRm9jRbvzuV%2FSw6kkaLmFkEhIvXpo0RKRLRYOdCHsh4b0xvJHtjbnp2Ugg0OiBfTGObcqrYALt15i0mzd1Gny4bA4rFZfeGveCSBxaZ1Bt9zw7rMiFENJrsPCge8U6Etm2feMt%2BDfsmTWBsdv13riJzk4v0V%2B%2FA%3D%3D',
        'tmr_detect': '0%7C1731931275044',
        'gsscgib-w-mvideo': 'solqE/6xkzHBond1Vc0NWqb3YB4sQ3xwK3f5DEDw+Pc2FXyGUCmaHtquljyHzhq1+xbIY8l4VNuGgojQO1HWQ6SQTFid2zAccP3IrxNVxNo7Vroy8bzhNyaWbd1XdWR+DHrupnBslDKvSjG4YiR5QJ+Wgb0UAfz4nZKHyLoI2/2yveV6ItsKZWdqf6hcxwcBOf0PBZ7vwsb5/FRRu6CYd4z5JoWnhlnJ27c+6HAZuNw7WcZEhfxidQgpyz0cb1wiylhwqlrK',
        'gsscgib-w-mvideo': 'solqE/6xkzHBond1Vc0NWqb3YB4sQ3xwK3f5DEDw+Pc2FXyGUCmaHtquljyHzhq1+xbIY8l4VNuGgojQO1HWQ6SQTFid2zAccP3IrxNVxNo7Vroy8bzhNyaWbd1XdWR+DHrupnBslDKvSjG4YiR5QJ+Wgb0UAfz4nZKHyLoI2/2yveV6ItsKZWdqf6hcxwcBOf0PBZ7vwsb5/FRRu6CYd4z5JoWnhlnJ27c+6HAZuNw7WcZEhfxidQgpyz0cb1wiylhwqlrK',
        '_sp_id.d61c': '1f7cc94c-3946-4441-8d1c-03f394e3de74.1725712944.5.1731931317.1731756059.84439cdd-295f-449b-9402-6b471840f130.c43dca8c-6027-46c1-8469-053c2227696b.b7ca61ff-4308-4233-9dba-e0cd41f564f4.1731931202519.97',
        'fgsscgib-w-mvideo': 'cLqIc31c78b9406eb0f48de6a5ceb8a9e13945d7',
        'fgsscgib-w-mvideo': 'cLqIc31c78b9406eb0f48de6a5ceb8a9e13945d7',
        'gsscgib-w-mvideo': 'HJyLgRWJOoVchqJxZlr2O4679zkzqUiKiwRSOvinhHTz6i7Skvih8Efi87TcaEEbg7vMrWERHBeS+2A3blWx/DqG0rBr2JFL69mVwln6vU1nSO0BOkbgkGZalM08/+gfKSOLnMJwszkCv9TPAtbSwgfKLwVQnktajCllDfMpUmrar/NHf/QT9wtYjLCZVveMQehOXIj9lY93gSDaCTE1D+WhUQYX1VS6+0vYpvO/AaMrK38A5CJ1RbgNX5+B6wBPQl25eKms',
        'cfidsgib-w-mvideo': 'FCzTwxuf902MYjcoh8Pu3TAhwE6+dLNk5xyeqUmexlmw66A0rEJtUZUd0MG/16Ge1tJzEQIJ47L2dAfut9M8tU+0Bx7Gk7hFs9dT9tMIYkoU9qmwbb4TV3/v7vqYf6Vg3OZQdE+ssA0wzoUZSQFnnbOqHGWN6bzdSO+hDw==',
        '_ga_CFMZTSS5FM': 'GS1.1.1731931202.5.1.1731931318.0.0.0',
        '_ga_BNX5WPP3YK': 'GS1.1.1731931202.5.1.1731931318.7.0.0',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'baggage': 'sentry-environment=production,sentry-release=release_24_11_2(9495),sentry-public_key=ae7d267743424249bfeeaa2e347f4260,sentry-trace_id=872b9eba2eb54254a5f8b21eaf20af76,sentry-sample_rate=0.1,sentry-transaction=%2F**%2F,sentry-sampled=false',

        'priority': 'u=1, i',
        'referer': 'https://www.mvideo.ru/televizory-i-cifrovoe-tv-1/televizory-65?f_tolko-v-nalichii=da&f_skidka=da',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '872b9eba2eb54254a5f8b21eaf20af76-b7d1d0a887233e14-0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-set-application-id': '4332a1fa-0c84-41a3-a3f6-c436bbfa2fb1',
    }

    params = {
        'categoryId': '65',
        'offset': '0',
        'limit': '24',
        'filterParams': [
            'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
            'WyJza2lka2EiLCIiLCJkYSJd',
        ],
        'doTranslit': 'true',
    }

    response = requests.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies, headers=headers).json()
    products_ids = response.get('body').get('products')
    with open('products.json', 'w', encoding="utf-8") as file:
        json.dump(products_ids, file, indent=4, ensure_ascii=False)

    json_data = {
        'productIds': products_ids,
        'mediaTypes': [
            'images',
        ],
        'category': True,
        'status': True,
        'brand': True,
        'propertyTypes': [
            'KEY',
        ],
        'propertiesConfig': {
            'propertiesPortionSize': 5,
        },
    }

    response = requests.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies, headers=headers, json=json_data).json()
    with open('2_products.json', 'w', encoding="utf-8") as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    products_ids_str = ','.join(products_ids)

    params = {
        'productIds': products_ids_str,
        'addBonusRubles': 'true',
        'isPromoApplied': 'true',
    }

    response = requests.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                            headers=headers).json()
    with open('3_products.json', 'w', encoding="utf-8") as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    items_prices = {}

    material_prices = response.get('body').get('materialPrices')

    for item in material_prices:
        item_id = item.get('price').get('productId')
        item_base_price = item.get('price').get('basePrice')
        item_sale_price = item.get('price').get('salePrice')
        item_bonus = item.get('bonusRubles').get('total')

        items_prices[item_id] = {
            'item_basePrice': item_base_price,
            'item_salePrice': item_sale_price,
            'item_bonus': item_bonus

        }
    with open('4_products.json', 'w', encoding="utf-8") as file:
        json.dump(items_prices, file, indent=4, ensure_ascii=False)


def get_result(url=None):
    with open('2_products.json') as file:
        products_data = json.load(file)
    with open('4_products.json') as file:
        products_prices = json.load(file)

    products_data = products_data.get('body').get('products')

    for item in products_data:
        product_id = item.get('productId')

        if product_id in products_prices:
            prices = products_prices[product_id]

        item['item_basePrice'] = prices.get('item_basePrice'),
        item['item_salePrice'] = prices.get('item_salePrice'),
        item['item_bonus'] = prices.get('item_bonus')

    with open('5_products.json', 'w') as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    get_result()


if __name__ == '__main__':
    main()