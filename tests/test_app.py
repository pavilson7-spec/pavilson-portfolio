import unittest

from app import app


class PortfolioAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page_renders(self):
        response = self.client.get("/")
        body = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Pavilson S", body)
        self.assertIn("Pavilson Is Here", body)
        self.assertIn("/static/resume/Pavilson_Software_Developer_Resume.pdf", body)

    def test_health_route(self):
        response = self.client.get("/health")
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["status"], "ok")

    def test_chat_rejects_blank_messages(self):
        response = self.client.post("/chat", json={"message": "   "})
        payload = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("Please enter a message", payload["response"])
        self.assertTrue(payload["actions"])

    def test_chat_returns_project_guidance(self):
        response = self.client.post("/chat", json={"message": "Explain the MindNest AI Application."})
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("MindNest", payload["response"])
        self.assertTrue(any(action["kind"] == "navigate" for action in payload["actions"]))

    def test_chat_returns_contact_details(self):
        response = self.client.post("/chat", json={"message": "How can I contact Pavilson?"})
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("+91 8667840473", payload["response"])
        self.assertIn("pavilson7@gmail.com", payload["response"])

    def test_static_assets_are_served(self):
        resume = self.client.get("/static/resume/Pavilson_Software_Developer_Resume.pdf")
        certificate = self.client.get("/static/certificates/Pavilson_Canza_Internship_Certificate.jpg")
        profile = self.client.get("/static/images/pavilson-profile.png")

        self.assertEqual(resume.status_code, 200)
        self.assertEqual(certificate.status_code, 200)
        self.assertEqual(profile.status_code, 200)

        resume.close()
        certificate.close()
        profile.close()


if __name__ == "__main__":
    unittest.main()
