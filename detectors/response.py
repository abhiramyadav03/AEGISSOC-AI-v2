RESPONSE_ACTIONS = {

    "Failed Login": [
        "Check user account.",
        "Verify if the source IP is trusted.",
        "Monitor for additional login attempts."
    ],

    "Brute Force Attack": [
        "Block the source IP.",
        "Disable the targeted account if necessary.",
        "Collect related authentication logs.",
        "Escalate to SOC Tier-2."
    ],

    "Admin Privilege Assigned": [
        "Verify whether the privilege assignment was authorized.",
        "Review recent administrator activity.",
        "Check for suspicious account changes."
    ],

    "New User Created": [
        "Verify the account creation request.",
        "Check group memberships.",
        "Review recent administrative actions."
    ]
}