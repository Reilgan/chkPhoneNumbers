import random
import json
from telegram.client import Telegram
import time


if __name__ == '__main__':
    print("Start")

    with open('data.json') as json_file:
        data = json.load(json_file)

    newData = []
    activNum = 0
    start_num = None
    for i, _ in enumerate(data):
        activNum += 1
        if _.get("activ", None) and _["activ"] is True:
            start_num = i
            break
    print("start_num: ", start_num)
    newData = data[start_num:]

    chunk = 30
    contacts_packs = zip(*[iter(newData)] * chunk)

    tg = Telegram(
        api_id=7461521,
        api_hash='f43cb392ed98997856e4174ba48d43a0',
        phone='+79080578569',
        database_encryption_key='Reilgan',
        # use_test_dc=True
    )
    tg.login()

    new_start_num = start_num
    for pack in contacts_packs:
        contacts = [{"phone_number": str(x["phone"]), "first_name": str(x['id'])} for x in pack]
        res = False
        while res is False:
            response = tg.call_method('importContacts', {
                'contacts': contacts
            })
            response.wait()
            if response.error:
                print(response.error_info)
                if response.error_info['code'] == 429:
                    timeout = response.error_info['message'].split(' ')[5]
                    if float(timeout) == 3600:
                        data[start_num]['activ'] = False
                        data[new_start_num]['activ'] = True
                        with open('data.json', 'w') as outfile:
                            json.dump(data, outfile)
                        print("Restart")
                        time.sleep(5)
                        quit()
                    time.sleep(float(timeout))
                time.sleep(10)
            else:
                res = True

        print(response.update)
        for user_id, imp_count, contact in zip(response.update['user_ids'], response.update['importer_count'], contacts):
            contact["user_id"] = user_id
            contact["importer_count"] = imp_count

        with open('result1.txt', 'a') as file:
            for contact in contacts:
                file.write(str(contact) + '\n')

        new_start_num += len(contacts)

        time.sleep(random.randint(5, 10))




    # for phone in phones:
    #     res = False
    #     while res is False:
    #         response = tg.call_method('importContacts', {
    #             'contacts': [
    #                 {'phone_number': phone['phone']},
    #             ]
    #         })
    #         response.wait()
    #         if response.error:
    #             print(response.error_info)
    #             if response.error_info['code'] == 429:
    #                 timeout = response.error_info['message'].split(' ')[5]
    #                 time.sleep(float(timeout))
    #         else:
    #             res = True
    #
    #     user_ids = response.update['user_ids']
    #
    #     print(user_ids, phone['phone'])
    #
    #     if user_ids[0] == 0:
    #         phone['inTelegram'] = True
    #     else:
    #         phone['inTelegram'] = False
    #
    #     tg.call_method('removeContacts', {'user_ids': user_ids})
    #
    #     w = dict(phone=phone['phone'], fact_repayment_date=phone['fact_repayment_date'], inTelegram=phone['inTelegram'])
    #
    #     with open('result.txt', 'a') as file:
    #         file.write(str(w) + '\n')
    #
    #     time.sleep(5)


