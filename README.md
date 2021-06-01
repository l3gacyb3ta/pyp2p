# pyp2p

## Commands:
```
/sync                       - Sync the identity data (happens on login)
/save                       - Saves the identity file
/load                       - Loads the identity file
/exit                       - Quits, and sends a signoff message
```

## Packet data:  
Just a string: Just push it out  
If it has a ~~ in the begginig its a thing the computer needs to deal with  
  
These packets are:  
- `~~setname~~`: This takes two arguments, the first is the nickname, and the second is the ip
- `~~sync~~`: This causes nodes to send out `~~setname~~` tokens for their peeps list.