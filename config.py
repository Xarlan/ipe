from datetime import timedelta


class Config:
    # secret key
    SECRET_KEY = '2c6aa3069c474cf38872c6e1dfa7a044'
    # max size of upload attachment
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    # Session cookie settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    REMEMBER_COOKIE_SAMESITE = 'Strict'

    # Change SESSION_COOKIE_SECURE and  REMEMBER_COOKIE_SECURE to True after ssl/tls certificate implementation
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

    # Database settings
    SQLALCHEMY_DATABASE_URI = "postgresql://ipeuser:ipeuser@localhost:5432/ipe"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Protocol for AJAX communication. If You use TLS certificate - change to "https://", else - "http://"
    SERVER_PROTO = "http://"
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = "5000"

    # ssl/tls certificate
    IPE_CERT = ""
    # ssl/tls key
    IPE_KEY = ""
