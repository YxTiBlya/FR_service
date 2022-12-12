import asyncio, time, datetime, requests, logging, os
from dotenv import load_dotenv

from sweater import db, app, token, service
from sweater.models import Mailings, Contacts, Messages

load_dotenv()
logger = logging.getLogger("mailer")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/logs.log", mode="a")
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def mailer(mailing):
    filters = list(map(lambda filter: filter.strip(), mailing.filters.split(",")))
    contacts = Contacts.query.filter(Contacts.tag.in_(filters)).all()
    print(contacts)

    for contact in contacts:
        datetime_now = datetime.datetime.now()

        if datetime_now > mailing.end_time: break

        r = requests.get(f"{os.environ.get('API_ADDRES')}/api/messages", json={"query": [mailing.id, contact.id]})

        if r.status_code == 400:
            my_r = requests.post(f"{os.environ.get('API_ADDRES')}/api/messages", json={"datetime": str(datetime_now), "status": "Ожидается", "mailing_id": mailing.id, "contact_id": contact.id})

            message_id = my_r.json()["id"]
            service_r = requests.post(f"{service}/{message_id}", json={"id": message_id, "phone": contact.number, "text": mailing.message}, headers={"Authorization": token})

            if service_r.status_code == 200:
                requests.put(f"{os.environ.get('API_ADDRES')}/api/messages", json={"change": message_id, "status": "Успешно"})
                logger.info(f"post {service}/{message_id} {mailing.id}-mailing 200")
            else:
                requests.put(f"{os.environ.get('API_ADDRES')}/api/messages", json={"change": message_id, "status": "Не отправлено"})
                logger.info(f"post {service}/{message_id} {mailing.id}-mailing 400")
        else:
            message = r.json()
            if message["status"] != "Успешно":
                service_r = requests.post(f"{service}/{message['id']}", json={"id": message['id'], "phone": contact.number, "text": mailing.message}, headers={"Authorization": token})

                if service_r.status_code == 200:
                    requests.put(f"{os.environ.get('API_ADDRES')}/api/messages", json={"change": message['id'], "status": "Успешно"})
                    logger.info(f"post {service}/{message['id']} {mailing.id}-mailing 200")
                else:
                    requests.put(f"{os.environ.get('API_ADDRES')}/api/messages", json={"change": message['id'], "status": "Не отправлено"})
                    logger.info(f"post {service}/{message['id']} {mailing.id}-mailing 400")
            else:
                continue


async def main():
    with app.app_context():
        mailings = Mailings.query.all()

        if mailings == None:
            print("No mailings")
        else:
            print(mailings)

            datetime_now = datetime.datetime.now()
            for mailing in mailings:
                if datetime_now >= mailing.start_time and datetime_now <= mailing.end_time:
                    mailer(mailing)

if __name__ == "__main__":
    while True:
        asyncio.run(main())
        time.sleep(60)
