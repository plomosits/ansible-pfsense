
def diag_defaults(connection):
    connection.post(
        "/diag_defaults.php",
        {
            "Submit": " Yes "
        }
    )
