# Chat Application

The following repository consists of a chat-client application. The server is provided by the Vrije Universiteit Amsterdam.

## Requirements

The chat client must meet the following requirements:

1. Connect to the chat server and log in using a unique name.
2. Ask for another name is the chosen name is already taken.
3. Shutdown the client by typing !quit.
4. List all currently logged-in users by typing !who.
5. Send messages to other users by typing @username message.
6. Receive messages from other users and display them to the user.

## Chat Application Protocol

| Message                      | Sent by | Description                                                                                                                        |
| ---------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| HELLO-FROM <name>\n          | Client  | First hand-shake message.                                                                                                          |
| HELLO <name>\n               | Server  | Second hand-shake message.                                                                                                         |
| WHO\n                        | Client  | Request for all currently logged-in users.                                                                                         |
| WHO-OK <name1>,...,<namen>\n | Server  | A list containing all currently logged-in users.                                                                                   |
| SEND <user> <msg>\n          | Client  | A chat message for a user. Note that the message cannot containthe newline character, because it is used as the message delimiter. |
| SEND-OK\n                    | Server  | Response to a client if their ‘SEND’ message is processedsuccessfully.                                                             |
| UNKNOWN\n                    | Server  | Sent in response to a SEND message to indicate that thedestination user is not currently logged in.                                |
| DELIVERY <user> <msg>\n      | Server  | A chat messagefroma user.                                                                                                          |
| IN-USE\n                     | Server  | Sent during handshake if the user cannot log in because thechosen username is already in use.                                      |
| BUSY\n                       | Server  | Sent during handshake if the user cannot log in because themaximum number of clients has been reached.                             |
| BAD-RQST-HDR\n               | Server  | Sent if the last message received from the client contains an errorin the header.                                                  |
| BAD-RQST-BODY\n              | Server  | sent if the last message received from the client contains an errorin the body.                                                    |

Table 1: Chat Application Protocol. Angular brackets (<>) indicate variable content.
