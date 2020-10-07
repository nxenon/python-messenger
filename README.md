# Python Multi User GUI Messenger
- GUI messenger app for both server and clients
# Features :
- Checking clients messages from server `Shell`
- Displaying connected clients
- Send server and client signal for cheking connection between them
- The server logs client `connections status and attempts` in `logs/connections.log`
- The log file will be created after you execute the ServerGUI.py
- Password authentication `(optional)`
# Note 
- Default port is `54321` but you can change the port
- After opening the `Chat Room` window , press `Connect` button for trying to connect to the server
- Usernames and passwords are `case-sensitive` !
# When Authentication Is Enabled
- Usernames and paaswords are stored in `creds.txt` file you can add or remove users .
- By default there are 2 usernames : test and test2 (you can remove them)
# To Run The App :
# Server Side : 
- 1)Open `ServerGUI.py` and enter IP and port number, press `Start` for listening
- 2)Then start `ClientGUI.py` , connect the clients and you can see them in clients list 
- ![Screenshot](images/server_img1.png) 

# Client Side :
- 1)Enter the information (password authentication is `optional`)
- If you want use password check the `authentication enabled` check box
- 2)Press `Set`
- ![Screenshot](images/client_img1_connect_box.png)
- 3)Press `Connect` to connect to the server
- 4)Then you can send and receive messages from connected clients
- ![Screenshot](images/client_img2_connect_guide.png)
