from django.test import TestCase
from rest_framework import status
from eszone_ipf.settings import BASE_DIR, API_VERSION_PREFIX


class ConfigFileTestCase(TestCase):
    url = '/{}/api_ipf/config/'.format(API_VERSION_PREFIX)
    url_act = ''.join([url, 'activate/'])

    def test_ipf_form_post(self):
        title = 'test_ipf.conf'
        test_file = ''.join([BASE_DIR, title])

        with open(test_file, 'w+') as f:
            f.write('# Test file.')
            f.seek(0)
            files={'title':     (title, ''),
                   'form':      ('ipf', ''),
                   'directory': (title, f.read())}
        response = self.client.post(self.url, files=files)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ipnat_form_post(self):
        title = 'test_ipnat.conf'
        test_file = ''.join([BASE_DIR, title])

        with open(test_file, 'w+') as f:
            f.write('# Test file.')
            f.seek(0)
            files={'title':     (title, ''),
                   'form':      ('ipnat', ''),
                   'directory': (title, f.read())}
        response = self.client.post(self.url, files=files)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ippool_form_post(self):
        title = 'test_ippool.conf'
        test_file = ''.join([BASE_DIR, title])

        with open(test_file, 'w+') as f:
            f.write('# Test file.')
            f.seek(0)
            files={'title':     (title, ''),
                   'form':      ('ippool', ''),
                   'directory': (title, f.read())}
        response = self.client.post(self.url, files=files)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ipf6_form_post(self):
        title = 'test_ipf6.conf'
        test_file = ''.join([BASE_DIR, title])

        with open(test_file, 'w+') as f:
            f.write('# Test file.')
            f.seek(0)
            files={'title':     (title, ''),
                   'form':      ('ipf6', ''),
                   'directory': (title, f.read())}
        response = self.client.post(self.url, files=files)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_form_post(self):
        title = 'test_ipf.conf'
        test_file = ''.join([BASE_DIR, title])

        with open(test_file, 'w+') as f:
            f.write('# Test file.')
            f.seek(0)
            files={'title':     (title, ''),
                   'form':      ('wrong', ''),
                   'directory': (title, f.read())}
        response = self.client.post(self.url, files=files)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_arg_post(self):
        files={'title':     ('wrong', ''),
               'form':      ('wrong', '')}
        response = self.client.post(self.url, files=files)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_conf_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_conf_file(self):
        response = self.client.get(''.join([self.url, 'test_ipf.conf/']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_existing_conf_file(self):
        response = self.client.get(''.join([self.url, 'no_test.conf/']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_conf_file(self):
        title = 'test_ipf.conf'
        test_file = ''.join([BASE_DIR, title])

        with open(test_file, 'w+') as f:
            f.write('# Test file.')
            f.seek(0)
            files={'title':     (title, ''),
                   'directory': (title, f.read())}
        response = self.client.put(''.join([self.url, 'test_ipf.conf/']),
                                   files=files)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_conf_file(self):
        response = self.client.delete(''.join([self.url, 'test_ipf.conf/']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_activate_ipf_form(self):
        response = self.client.get(''.join([self.url_act, 'test_ipf.conf/']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_ipnat_form(self):
        response = self.client.get(''.join([self.url_act, 'test_ipnat.conf/']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_ippool_form(self):
        response = self.client.get(''.join([self.url_act, 'test_ippool.conf/']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_ipf6_form(self):
        response = self.client.get(''.join([self.url_act, 'test_ipf6.conf/']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogFileTestCase(TestCase):
    url = '/{}/api_ipf/log/'.format(API_VERSION_PREFIX)
    title = 'test.log'

    def test_post(self):
        response = self.client.post(self.url, data={'title': self.title})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_arg_post(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_log_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_log_file(self):
        response = self.client.get(''.join([self.url, 'test.log/']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_existing_log_file(self):
        response = self.client.get(''.join([self.url, 'no_test.log/']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_log_file(self):
        response = self.client.delete(''.join([self.url, 'test.log/']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OtherTestCase(TestCase):
    url = '/{}/api_ipf/'.format(API_VERSION_PREFIX)

    def test_blacklist_update(self):
        response = self.client.get(''.join([self.url, 'update/']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_allowed_command(self):
        response = self.client.get(''.join([self.url, 'command/ipfstat -io/']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_allowed_command(self):
        response = self.client.get(''.join([self.url, 'command/pkill python/']))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)