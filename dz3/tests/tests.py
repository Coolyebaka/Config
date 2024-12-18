#python3 -m unittest tests/test.py

import unittest
from main import ConfigParser

class TestConfigParser(unittest.TestCase):
    def test_web_server_config(self):
        input_text = '''
        set PORT = 8080;
        dict :=
            begin
                port := #(PORT);
                ssl_enabled := 1;
            end
        '''
        parser = ConfigParser()
        parser.parse_input(input_text)
        toml_output = parser.to_toml()
        expected_output = '''
        [dict]\nport = 8080\nssl_enabled = 1
        '''
        self.assertEqual(toml_output.strip(), expected_output.strip())

    def test_database_config(self):
        input_text = '''
        set DB_PORT = 5432;
        set DB_USER = 1;
        set DB_PASS = 12345678;

        dict :=
            begin
                port := #(DB_PORT);
                credentials :=
                    begin
                        user := #(DB_USER);
                        password := #(DB_PASS);
                    end
            end
        '''
        parser = ConfigParser()
        parser.parse_input(input_text)
        toml_output = parser.to_toml()
        expected_output = '''
        [dict]\nport = 5432\n[dict.credentials]\nuser = 1\npassword = 12345678
        '''
        self.assertEqual(toml_output.strip(), expected_output.strip())


if __name__ == "__main__":
    unittest.main()
