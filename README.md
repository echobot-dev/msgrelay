# Message Relay for Echobot

*Part of project Echobot.*

> Note: This is a pre-release version, and is not yet ready for production use.

## Features

- [x] Cross-platform message relay.
- [x] Broadcast messages to all connected bot instances.
- [x] Specify channels to allow messages to be relayed.
- [x] Configure relay message format (header, footer, etc.) for each type of adapter.
- [ ] Unidirectional relay (receive / send only).
- [ ] Specify source / destination channels for relayed messages.

## Supported adapters

- [x] OneBot V11
- [x] Discord

### Known limitations

- OneBot V11
  - Forward / custom forward messages are not supported to be relayed as source message.
- Discord
  - Attachments are not supported to be relayed as source message.
