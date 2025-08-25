# adopted from https://github.com/lbr88/mattermost-chillzone-1337bot/commit/301ea0693e709d89f49b2658d62c246b062f3da3
# https://github.com/Vaelor/python-mattermost-driver/issues/115
# monkey patching ssl.create_default_context to fix SSL error
# to fix:
# bot-1    | [2024-02-12-14:41:46][websockets.client][DEBUG] = connection is CONNECTING
# bot-1    | [2024-02-12-14:41:46][mattermostdriver.websocket][WARNING] Failed to establish websocket connection: Cannot create a client socket with a PROTOCOL_TLS_SERVER context (_ssl.c:811)
import ssl

# save the original create_default_context function so we can call it later
create_default_context_orig = ssl.create_default_context


# define a new create_default_context function that sets purpose to ssl.Purpose.SERVER_AUTH
def cdc(*args, **kwargs):
    kwargs["purpose"] = ssl.Purpose.SERVER_AUTH
    return create_default_context_orig(*args, **kwargs)


# monkey patching ssl.create_default_context to fix SSL error
ssl.create_default_context = cdc
