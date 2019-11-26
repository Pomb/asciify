import asciify.settings as settings
import unittest


class SimpleTest(unittest.TestCase):

    def test(self):
        self.assertEqual(settings.application["width"], 1024)
        self.assertEqual(settings.application["height"], 600)


if __name__ == "__main__":
    unittest.main()
