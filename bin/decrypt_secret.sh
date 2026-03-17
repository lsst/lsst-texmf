#!/bin/sh
# encrypt with  gpg -c token.pickle
# Decrypt the file
# --batch to prevent interactive command
# --yes to assume "yes" for questions
# if used in GA make sure TOKEN_PASSPHRASE is set in the repo secrets to
# match the pharse used to encrypyt token.pickle in the first place
gpg --quiet --batch --yes --decrypt --passphrase="$TOKEN_PASSPHRASE" \
	--output token.pickle token.pickle.gpg
