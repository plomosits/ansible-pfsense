#!/usr/bin/python


def reboot(connection, rebootmode="Reboot"):
    connection.post(
        "/diag_reboot.php",
        {
            "rebootmode": rebootmode,
        }
    )
