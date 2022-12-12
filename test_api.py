import unittest, requests, os
from dotenv import load_dotenv

load_dotenv()
#cmd python -m unittest -v -b -f test_api.py
class TestApiRequests(unittest.TestCase):
    def test_contact(self):
        url = f"{os.environ.get('API_ADDRES')}/api/contact"

        r = requests.post(url, json={"number":"+7917235678", "operator_code":"917", "tag":"", "time_zone":""})
        self.assertEqual(r.status_code, 200)
        c_id = r.json()["id"]

        r = requests.post(url, json={"number":"+7917235678", "operator_code":"917", "tag":"", "time_zone":""})
        self.assertEqual(r.status_code, 400)

        r = requests.put(url, json={"change": c_id, "tag": "normal", "time_zone": "+6", "number":"+791723534"})
        self.assertEqual(r.status_code, 200)

        r = requests.delete(url, json={"id": c_id})
        self.assertEqual(r.status_code, 200)

        r = requests.delete(url, json={"id": 999})
        self.assertEqual(r.status_code, 400)

    def test_mailing(self):
        url = f"{os.environ.get('API_ADDRES')}/api/mailing"

        r = requests.post(url, json={"start_time": "2022-12-10 17:00:00", "message": "Тестовое сообщение", "filters": "tag, tag2", "end_time": "2022-12-10 19:30:00"})
        self.assertEqual(r.status_code, 200)
        m_id = r.json()["id"]

        r = requests.post(url, json={"start_time": "2022-12-10 17:00:00", "message": "Тестовое сообщение", "filters": "tag, tag2", "end_time": "2022-12-10 19:30:00"})
        self.assertEqual(r.status_code, 400)

        r = requests.post(url, json={"start_time": "2022-12-10 17:00:00", "message": "Тестовое сообщение", "filters": "", "end_time": "2022-12-10 19:30:00"})
        self.assertEqual(r.status_code, 400)

        r = requests.put(url, json={"change": m_id, "filters": "tag, tag2, tag2"})
        self.assertEqual(r.status_code, 200)

        r = requests.delete(url, json={"id": m_id})
        self.assertEqual(r.status_code, 200)

        r = requests.delete(url, json={"id": 999})
        self.assertEqual(r.status_code, 400)

    def test_messages(self):
        url = f"{os.environ.get('API_ADDRES')}/api/messages"

        r = requests.post(url, json={"datetime": "2022-12-10 17:00:00", "status": "Обработка", "mailing_id": 1, "contact_id": 3})
        self.assertEqual(r.status_code, 200)
        m_id = r.json()["id"]

        r = requests.get(url, json={"query": [1, 3]})
        self.assertEqual(r.status_code, 200)

        r = requests.put(url, json={"change": m_id, "status": "Не отправлено"})
        self.assertEqual(r.status_code, 200)


        r = requests.delete(url, json={"id": m_id})
        self.assertEqual(r.status_code, 200)

        r = requests.get(url, json={"query": [1, 3]})
        self.assertEqual(r.status_code, 400)