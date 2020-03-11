# chattingWithFriends
A simple app to chat with friends! Talk one-on-one with a friend or jump into a chat room!&nbsp;

Important Use Instructions:

-If hosting a server, port forwarding may be necessary\
-The port that the server binds to must be set in the serverProps.txt\
-Clients must know the external IP and port of the server before hand

v1.2
  
  -Chatting with Friends is no longer contrained to users on a LAN! Now users can chat anywhere in the world\
  -Functions in the server script were moved inside the class
  
v1.1

  -Server includes a function to retrieve private IP of the host. This will allow the server to be accessed by members of LAN\
  -Client has been updated concurrently accept and send messages to another instance of itself using threads

v1.0

  -Server and clients run on local host\
  -Each client sends one message and receives one message
  
  
Todo
  
  -Add ability to accept concurrent connections in server using threads\
  -Expand client display\
  -add friends list\
  -add login/registration\
  -add chatroom\
  -add a way to gracefully close client\
  -check possible exceptions and implement proper ways to handle such exceptions\
  -add GUI\
  -add security(TLS or end-to-end encryption)
  -transform into executable

  
