import unittest
from mock import patch
from app import _get_categories, _get_wallpapers_for_category


class MyTestCase(unittest.TestCase):
    def test_get_list_of_categories(self):
        with \
                patch('app.os.listdir', return_value=["xx", "yy", "yy"]),\
                patch('app.os.path.isdir', side_effect=[True, True, False]):
            self.assertCountEqual(["xx", "yy"], _get_categories())

    def test_get_list_of_category(self):
        with \
                patch('app.glob', return_value=["media/wallpapers/test/xx.jpg",
                                                "media/wallpapers/test/yy.jpg",
                                                "media/wallpapers/test/zz.jpg"]),\
                patch('app.os.path.isfile', side_effect=[True, False, True]):
            self.assertItemsEqual([
                ('wallpapers\\test\\xx.jpg', 'wallpapers\\test\\xx.mov'),
                ('wallpapers\\test\\zz.jpg', 'wallpapers\\test\\zz.mov'),
            ], _get_wallpapers_for_category('test'))


if __name__ == '__main__':
    unittest.main()
