curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
    "bot_email": "printer-bot@wesleyac.com",
    "data": "@**Printer Bot** test message!",
    "message": {
        "client": "website",
        "content": "@**Printer Bot** test message!",
        "display_recipient": "Verona",
        "id": 112,
        "is_me_message": false,
        "raw_display_recipient": "Verona",
        "reactions": [],
        "recipient_id": 20,
        "recipient_type": 2,
        "recipient_type_id": 5,
        "rendered_content": "<p><span class=\"user-mention\" data-user-id=\"25\">@Printer Bot</span> test message!</p>",
        "sender_avatar_source": "G",
        "sender_avatar_version": 1,
        "sender_email": "foo@foo.com",
        "sender_full_name": "Foo",
        "sender_id": 5,
        "sender_is_mirror_dummy": false,
        "sender_realm_id": 1,
        "sender_realm_str": "zulip",
        "sender_short_name": "foo",
        "stream_id": 5,
        "subject": "Verona2",
        "subject_links": [],
        "submessages": [],
        "timestamp": 1527876931,
        "type": "stream"
    },
    "token": "xvOzfurIutdRRVLzpXrIIHXJvNfaJLJ0",
    "trigger": "mention"
}' \
  http://localhost:8080/print
