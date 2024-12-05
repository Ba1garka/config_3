import json
import unittest
from collections import OrderedDict

class TestConfigurationLanguage(unittest.TestCase):

    db_config = '''{
        "constants": {
            "max_connections": 100,
            "timeout": 30,
            "retry_attempts": 5
        },
        "database": {
            "type": "sql",
            "host": "localhost",
            "port": 5432,
            "credentials": {
                "username": "admin",
                "password": "securepassword"
            },
            "options": {
                "ssl": true,
                "pool_size": 10,
                "log_queries": false
            }
        },
        "tables": [
            {
                "name": "users",
                "columns": {
                    "id": "integer",
                    "username": "string",
                    "email": "string",
                    "registered_at": "timestamp"
                },
                "constraints": {
                    "primary_key": "id",
                    "unique": ["username", "email"]
                }
            },
            {
                "name": "posts",
                "columns": {
                    "id": "integer",
                    "user_id": "integer",
                    "content": "text",
                    "created_at": "timestamp"
                },
                "constraints": {
                    "primary_key": "id",
                    "foreign_key": {
                        "field": "user_id",
                        "references": "users(id)"
                    }
                }
            }
        ]
    }'''

    web_app_config = '''{
        "constants": {
            "default_language": "en",
            "maintenance_mode": false,
            "cookie_expiration_days": 30
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8080,
            "routes": {
                "home": {
                    "method": "GET",
                    "path": "/",
                    "handler": "homeController.index"
                },
                "login": {
                    "method": "POST",
                    "path": "/login",
                    "handler": "authController.login"
                }
            },
            "middleware": [
                "logger",
                "bodyParser",
                "session"
            ]
        },
        "database": {
            "url": "mongodb://localhost:27017",
            "name": "my_web_app",
            "options": {
                "useNewUrlParser": true,
                "useUnifiedTopology": true
            }
        }
    }'''

    monitoring_config = '''{
        "constants": {
            "monitoring_interval": 60,
            "alert_threshold": 90,
            "email_notifications": true
        },
        "services": [
            {
                "name": "service_1",
                "type": "api",
                "url": "http://service-1.example.com/health",
                "check": {
                    "method": "GET",
                    "timeout": 5,
                    "expected_status": 200
                },
                "alerts": {
                    "email": {
                        "recipients": ["admin@example.com", "support@example.com"],
                        "subject": "Service 1 Down",
                        "body": "Service 1 is not responding as expected."
                    },
                    "sms": {
                        "recipient": "+1234567890",
                        "message": "Service 1 is down!"
                    }
                }
            },
            {
                "name": "service_2",
                "type": "database",
                "url": "http://service-2.example.com/health",
                "check": {
                    "method": "GET",
                    "timeout": 5,
                    "expected_status": 200
                },
                "alerts": {
                    "email": {
                        "recipients": ["admin@example.com"],
                        "subject": "Service 2 Down",
                        "body": "Service 2 is not responding as expected."
                    }
                }
            }
        ]
    }'''

    def setUp(self):
        self.db_config = json.loads(self.db_config, object_pairs_hook=OrderedDict)
        self.web_app_config = json.loads(self.web_app_config, object_pairs_hook=OrderedDict)
        self.monitoring_config = json.loads(self.monitoring_config, object_pairs_hook=OrderedDict)

    def test_database_config(self):
        config = self.db_config
        # Проверяем наличие ключей
        self.assertIn('constants', config)
        self.assertIn('database', config)
        self.assertIn('tables', config)

        # Проверяем значения в constants
        self.assertEqual(config['constants']['max_connections'], 100)
        self.assertEqual(config['constants']['timeout'], 30)

        # Проверяем параметры в database
        self.assertEqual(config['database']['type'], 'sql')
        self.assertEqual(config['database']['host'], 'localhost')

        # Проверяем таблицы
        self.assertEqual(len(config['tables']), 2)
        self.assertIn('users', [table['name'] for table in config['tables']])
        self.assertIn('posts', [table['name'] for table in config['tables']])

        # Проверяем вложенные ограничения
        users_table = config['tables'][0]
        self.assertIn('constraints', users_table)
        self.assertEqual(users_table['constraints']['primary_key'], 'id')

    def test_web_app_config(self):
        config = self.web_app_config
        # Проверяем наличие ключей
        self.assertIn('constants', config)
        self.assertIn('server', config)
        self.assertIn('database', config)

        # Проверяем значения в constants
        self.assertEqual(config['constants']['default_language'], 'en')
        self.assertFalse(config['constants']['maintenance_mode'])

        # Проверяем параметры в server
        self.assertEqual(config['server']['port'], 8080)
        self.assertIn('routes', config['server'])

        # Проверяем наличие маршрутов
        routes = config['server']['routes']
        self.assertIn('home', routes)
        self.assertIn('login', routes)

        # Проверяем middleware
        self.assertIn('logger', config['server']['middleware'])

    def test_monitoring_config(self):
        config = self.monitoring_config
        # Проверяем наличие ключей
        self.assertIn('constants', config)
        self.assertIn('services', config)

        # Проверяем значения в constants
        self.assertEqual(config['constants']['monitoring_interval'], 60)
        self.assertTrue(config['constants']['email_notifications'])

        # Проверяем наличие сервисов
        services = config['services']
        self.assertGreater(len(services), 0)

        # Проверяем параметры первого сервиса
        service_1 = services[0]
        self.assertEqual(service_1['name'], 'service_1')
        self.assertIn('check', service_1)

        # Проверяем настройки оповещений сервиса
        alert_email = service_1['alerts']['email']
        self.assertIn('recipients', alert_email)
        self.assertIn('subject', alert_email)

if __name__ == '__main__':
    unittest.main()
