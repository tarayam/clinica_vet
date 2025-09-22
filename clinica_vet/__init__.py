try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    # If PyMySQL isn't installed yet, this won't break anything.
    pass
