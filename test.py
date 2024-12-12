import json
import unittest
from datetime import datetime

class TestConfigurationLanguage(unittest.TestCase):

    def get_current_time(self):
        return datetime.now().isoformat()

    def test_db_config(self):
        current_time = self.get_current_time()
        db_config = '''{
            "time": "vrem",
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

        json_data = json.loads(db_config)
        json_data["time"] = current_time

        expected_output = f"(define vrem {current_time});\n" \
                          f"(define max_connections 100);\n" \
                          f"(define timeout 30);\n" \
                          f"(define retry_attempts 5);\n" \
                          f"{{\n" \
                          f"    time = q(vrem),\n"\
                          f"    database = {{\n" \
                          f"        type = q(sql),\n" \
                          f"        host = q(localhost),\n" \
                          f"        port = 5432,\n" \
                          f"        credentials = {{\n" \
                          f"            username = q(admin),\n" \
                          f"            password = q(securepassword)\n" \
                          f"        }},\n" \
                          f"        options = {{\n" \
                          f"            ssl = true,\n" \
                          f"            pool_size = 10,\n" \
                          f"            log_queries = false\n" \
                          f"        }}\n" \
                          f"    }}\n" \
                          f"}}"

        print(expected_output)

    def test_web_app_config(self):
        current_time = self.get_current_time()
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
                    },
                    "time": "vremia"
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

        json_data = json.loads(web_app_config)
        json_data["time"] = current_time

        expected_output = f"(define vremia {current_time});\n" \
                          f"(define default_language q(en));\n" \
                          f"(define maintenance_mode false);\n" \
                          f"(define cookie_expiration_days 30);\n" \
                          f"{{\n" \
                          f"    server = {{\n" \
                          f"        host = q(0.0.0.0),\n" \
                          f"        port = 8080,\n" \
                          f"        routes = {{\n" \
                          f"            home = {{\n" \
                          f"                method = q(GET),\n" \
                          f"                path = q(/),\n" \
                          f"                handler = q(homeController.index)\n" \
                          f"            }},\n" \
                          f"            login = {{\n" \
                          f"                method = q(POST),\n" \
                          f"                path = q(/login),\n" \
                          f"                handler = q(authController.login)\n" \
                          f"            }},\n" \
                          f"            time = q(vremia)\n"\
                          f"        }}\n" \
                          f"    }}\n" \
                          f"}}"

        print(expected_output)

    def test_monitoring_config(self):
        current_time = self.get_current_time()
        monitoring_config = '''{
            "constants": {
                "monitoring_interval": 60,
                "alert_threshold": 90,
                "email_notifications": true
            },
            "services": [
                {
                    "time": "current_time",
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

        json_data = json.loads(monitoring_config)
        json_data["time"] = current_time

        expected_output = f"(define current_time {current_time});\n" \
                          f"(define monitoring_interval 60);\n" \
                          f"(define alert_threshold 90);\n" \
                          f"(define email_notifications true);\n" \
                          f"{{\n" \
                          f"    services = [\n" \
                          f"        {{\n" \
                          f"            time = q(current_name),\n"\
                          f"            name = q(service_1),\n" \
                          f"            type = q(api),\n" \
                          f"            url = q(http://service-1.example.com/health),\n" \
                          f"            check = {{\n" \
                          f"                method = q(GET),\n" \
                          f"                timeout = 5,\n" \
                          f"                expected_status = 200\n" \
                          f"            }},\n" \
                          f"            alerts = {{\n" \
                          f"                email = {{\n" \
                          f"                    recipients = [\n" \
                          f"                        q(admin@example.com),\n" \
                          f"                        q(support@example.com)\n" \
                          f"                    ],\n" \
                          f"                    subject = q(Service 1 Down),\n" \
                          f"                    body = q(Service 1 is not responding as expected.)\n" \
                          f"                }},\n" \
                          f"                sms = {{\n" \
                          f"                    recipient = q(+1234567890),\n" \
                          f"                    message = q(Service 1 is down!)\n" \
                          f"                }}\n" \
                          f"            }}\n" \
                          f"        }},\n" \
                          f"        {{\n" \
                          f"            name = q(service_2),\n" \
                          f"            type = q(database),\n" \
                          f"            url = q(http://service-2.example.com/health),\n" \
                          f"            check = {{\n" \
                          f"                method = q(GET),\n" \
                          f"                timeout = 5,\n" \
                          f"                expected_status = 200\n" \
                          f"            }},\n" \
                          f"            alerts = {{\n" \
                          f"                email = {{\n" \
                          f"                    recipients = [\n" \
                          f"                        q(admin@example.com)\n" \
                          f"                    ],\n" \
                          f"                    subject = q(Service 2 Down),\n" \
                          f"                    body = q(Service 2 is not responding as expected.)\n" \
                          f"                }}\n" \
                          f"            }}\n" \
                          f"        }}\n" \
                          f"    ]\n" \
                          f"}}"

        print(expected_output)

if __name__ == '__main__':
    unittest.main()
