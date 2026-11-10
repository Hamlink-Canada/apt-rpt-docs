# Verify registration credentials in each registrar

Both registration services will support a local credential file or an authorized gRPC credential lookup, and verify the supplied password or IAX challenge response locally. This keeps IAX protocol semantics out of the future central server and permits a bounded 60-second credential cache during backend interruptions, at the cost of exposing retrieved passwords to authorized registrar processes and delaying password rotation or revocation until cache expiry; central verification was considered and rejected for this scope.
