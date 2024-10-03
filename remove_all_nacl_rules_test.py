import unittest
from unittest.mock import patch
import remove_all_nacl_rules
from botocore.exceptions import ClientError


class TestRemoveAllNaclRules(unittest.TestCase):
    describe_acl_return_value = {
        'NetworkAcls': [
            {
                'Entries': [
                    {'Egress': True, 'RuleNumber': 100}, {'Egress': True, 'RuleNumber': 32767},
                    {'Egress': False, 'RuleNumber': 200}, {'Egress': False, 'RuleNumber': 32767}
                ],
                'NetworkAclId': 'id'
            }
        ]
    }

    error_response = {'Error': {'Code': '500', 'Message': 'Server Error'}}

    @patch('remove_all_nacl_rules.client.describe_network_acls')
    @patch('remove_all_nacl_rules.client.delete_network_acl_entry')
    def test_remove_all_nacl_rules(self, delete_network_acl_entry, describe_network_acls):

        delete_network_acl_entry.return_value = {}
        describe_network_acls.return_value = self.describe_acl_return_value
        remove_all_nacl_rules.remove_all_nacl_rules()
        arg_list = delete_network_acl_entry.call_args_list

        self.assertEqual(arg_list[0][1]['RuleNumber'], 100)
        self.assertTrue(arg_list[0][1]['Egress'])

        self.assertEqual(arg_list[1][1]['RuleNumber'], 200)
        self.assertFalse(arg_list[1][1]['Egress'])

    @patch('remove_all_nacl_rules.client.describe_network_acls')
    @patch('remove_all_nacl_rules.client.delete_network_acl_entry')
    def test_error_if_describe_call_fails(self, delete_network_acl_entry, describe_network_acls):
        client_error = ClientError(self.error_response, 'DescribeNetworkAcls')

        describe_network_acls.side_effect = client_error
        with self.assertRaises(Exception) as ex:
            remove_all_nacl_rules.remove_all_nacl_rules()

        expected_error = 'An error occurred (500) when calling the DescribeNetworkAcls operation: Server Error'
        self.assertEqual(ex.exception.args[0], expected_error)

    @patch('remove_all_nacl_rules.client.describe_network_acls')
    @patch('remove_all_nacl_rules.client.delete_network_acl_entry')
    def test_error_if_delete_call_fails(self, delete_network_acl_entry, describe_network_acls):
        client_error = ClientError(self.error_response, 'DeleteNetworkAcls')

        describe_network_acls.return_value = self.describe_acl_return_value
        delete_network_acl_entry.side_effect = client_error
        with self.assertRaises(Exception) as ex:
            remove_all_nacl_rules.remove_all_nacl_rules()

        expected_error = 'An error occurred (500) when calling the DeleteNetworkAcls operation: Server Error'
        self.assertEqual(ex.exception.args[0], expected_error)
