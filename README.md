To understand the structure of our project, referencing Figures 1 and 2 will greatly help. There are two important systems running code: the Raspberry Pi and the aggregator (laptop/host system). Connected to our Pi is an Arduino and connected to our Arduino are two sensors, a DHT22 Sensor and a PS2 X Y Axis Sensor. The Arduino is a user-prescribed sensor. Currently, the Pi expects serial input from the Arduino in the form: “data|data|data|...|data”. This can be adjusted as is seen fit in socket_server.py.

Python is the main language which handles all of the processing on the PI and the aggregator. For these two systems to work there are a list of libraries that need to be installed for each of them to work. Since there is a decent amount of libraries needed, there is a requirements.txt inside the src folder that will list the needed libraries. To install all the libraries in the text file automatically, use “pip install -r requirements.txt”. This file includes the needed libraries for both the PI and Aggregator so the command should be run on both. If you have trouble installing these libraries, try using “pip3” instead of “pip”.

On both the PI and the aggregator we have an environment file to hold our sensitive data in variable names. An environment file is a file that you can reference in code to hold specific variables that should not have public access, such as passwords, IPs, etc as plain text. Meaning, you can have an environment variable named “password” that holds a password that looks like PASSWORD=HELLO123. For the PI, the .env file can be placed under the pi/ directory and on the aggregator, the .env file can be placed under the aggregator/ directory. The related .env files must look like this:

.env file for the Raspberry PI:

HOST=

PORT=

PRIVATE_KEY_ENROLLMENT=

UUID_ENROLLMENT=

HOST is the IP of the aggregator and PORT can be an arbitrarily chosen port to send the socket communication through. PRIVATE_KEY_ENROLLMENT is a variable that holds the private key of the sensor that was enrolled and UUID_ENROLLMENT is the unique ID that was created during enrollment as well. If a user wanted to add more sensors, they would just need to create more private key variables along with uuid variables.

.env file for the Aggregator:

CONTRACT_ADDRESS=

INFURA_API_KEY=

METAMASK_WALLET=

METAMASK_PRIV_KEY=

CONTRACT_ADDRESS will be explained in greater detail in the next paragraph, but for now this variable holds the hex address of the Solidity contract that was pushed onto the blockchain. For our purposes, we used the Ropsten testnet, which is a test blockchain that most similarly mimics the production Ethereum blockchain, meaning our contract address lives on this blockchain. With this, we needed an API that would connect us to the Ropsten test net, so we used a website called https://infura.io/. After setting up an account, an API key is needed to connect to the test net and this API key is held under the variable INFURA_API_KEY. To send data to the Ropsten blockchain, we needed a wallet with some Ethereum. We also set up a METAMASK wallet which was filled with some Ethereum through a faucet specifically for the Ropsten test net. The METAMASK wallet and private key are needed to send transactions and are held under the METAMASK_WALLET and METAMASK_PRIV_KEY variables respectively.

Once both an Infura and metamask account are set up, you can now deploy a contract to the blockchain, but before this, another step must be completed. Earlier, the private key and UUID of the sensor were mentioned and these must be created. On the PI, under the pi/ directory there is a file called sens_enroll.py which handles creating a UUID and private / public key pair for that sensor. One must execute this file only one time in the command line for each sensor and take note of the values that are printed to the console, which are the private key, and UUID just in case these are not properly stored in the environment variables. If not, one can copy and paste these values from the console into their .env file. Along with this, a file called enr.txt will be created under the pi/ directory which will hold the public key in the first line and sensor UUID on the next line. This was done to circumvent the issue of wired enrollment, so this file must be placed on a USB and transferred over to the aggregator to be parsed from there.

After the sensor enrollment setup is completed, one can now deploy their contract to the blockchain. To do this, one has to navigate to the website remix.ethereum.org. There are many tutorials on how to deploy a contract to the Ropsten test net blockchain using Remix that may be better than the explanation now if it is a little confusing. Also, as a side note, everything done here can be done using the main Ethereum blockchain blockchain, we are using the Ropsten test net to avoid using any real money for this project. Once a .sol file has been created on Remix, it is important to make sure it complies under the “Solidity Compiler” tab on the left. If it does, then you can head to the tab under the “Solidity Compiler” one named “Deploy & Run Transactions”. In this tab, you need to select your environment as “Injected Web3” then a METAMASK Chrome extension should open (if it is installed) if you need to enter your password. Once this has been done, clicking the “Deploy” button should open the Chrome METAMASK extension one last time to confirm that it is okay to spend the Ethereum to deploy this contract. Once the contract is deployed, it needs to get mined on the blockchain. In the meantime, in the Remix console there should be an item that says “view on therscan”. Clicking this should bring you to etherscan where you can see where the contract was deployed along with the address it was sent from (METAMASK wallet) and the address it was sent to (contract address). The contract address that was just created must be copied and pasted into the .env file under the CONTRACT_ADDRESS variable and should look something along the lines of “CONTRACT_ADDRESS=0x5e18a0f4a17a04771210847e46799ffec36dec7b” as an example.

The final piece that needs to be done is grabbing the ABI for the contract. Going back under the “Solidity Compiler” tab, make sure the .sol file is compiled and click the “Compilation Details” button on the bottom left hand corner of the screen. After clicking this, it should open a new window and from there “WEB3 DEPLOY” must be clicked. Under this new tab, the first line should contain some javascript code that looks like this: “var sensor_enrollmentContract = new web3.eth.Contract([]);”. The only values we’re concerned with is the text between the “[“ left bracket and “]” right bracket. After copying it should look something like:

[{"constant":false,"inputs"... etc}]

as a long JSON object. This is called the ABI code and must be placed in our code to work. This ABI must be placed in the aggregator under the aggreagator/src/ directory in the file contract_access.py. In that file, there is a line in the init function that declares a variable abi and assigns it a value. From what was shown above, this line should look like:

abi = json.loads('[{"constant":false,"inputs"... etc}]')

After this has been done, all of the setup related to the Ethereum contract is done. Under the contract_access.py a user would need to change the related methods to match the contract that was just created, but the contract that was provided can be used as a reference (above in contract_acces.py there is a commented piece of Solidity code that was used for our contract along with methods for storing and retrieving data).

Given the structure of our PI code, if a user wanted to add a new sensor to our project, they would need to add a python file under the pi/sensors/ directory which must contain a class that would fetch the data from whatever sensor they used, and have a method to return this data back to socket_client.py. In socket_client.py, one would need to define an instance of the class they just created, and call their related members to get the data. After this, the data would need to be sent into signed_data.py to turn the raw string data into a JSON object. Once everything above has been implemented, the user would need to run socket_client.py on the PI to create the socket connection between it and the aggregator. To fully establish the connection, the related aggregator.py file on the aggregator would need to be executed around the same time as the socket_client.py is executed. Once this is done, both the PI and aggregator will now be communicating the data from the Arduino to the aggregator through the socket connection.

As discussed earlier, the PI creates an enr.txt file that is transferred via USB to the aggregator which contains the enrollment information from a sensor. Now that the contract is deployed, a sensor can be enrolled through this file. This file should be under the aggregator/src directory as enr.txt and should contain the public key of the sensor as the first line and the UUID of the sensor as the second line. If all is correct, then the file enrollment.py, under the same directory, needs to be executed in the terminal. This file should print the public key and UUID to the terminal along with the transaction hash from the transaction that was created to send this data to the blockchain. Along with these values, the key should also print to the terminal as a confirmation that it was stored onto the blockchain since we make a call to the blockchain to retrieve the key given the sensor ID.

This project currently uses an SQL database (MySQL). However, it could be reconfigured to work with any other style of database, provided the user has knowledge of integrating one with python. When the database is created, the user can change the credentials within PyDbConn.py in order to connect their database to the sensor setup. Once properly initialized, no changes will need to be made to the SQL server.

Once data is stored on the blockchain, it can be accessed using the provided Flask server, or by a user-defined website. The given flask server can be run by executing servermain.py, and can be reached via your web browser at the IP: 127.0.0.1:5000. The default site is a simple date picker to select a date to pull data from. This can be modified to meet the needed requirements - the data pulling and processing is all completed within servermain.py. The pre-defined functions for retrieving data allow for ease of access, and ease of customization.

Further Improvements

For those who wish to develop this design for further applications, data transmission between the Arduino and the PI can be found under the pi/sensors/ directory in our provided code. There, we have a file named ‘arduino_sensor.py’ which holds a class that allows us to receive data from the Arduino.

This class is referenced under our pi/ directory in the file ‘socket_client.py’. This file establishes a socket connection between the PI and aggregator, using the class in the ‘arduino_sensor.py’ to call its related member to get the cleaned data from our Arduino.

Along with this, socket_client.py references another file under the pi/ directory named signed_data.py which takes the data that was given from the sensor, and returns it in a JSON format to be sent over the socket connection. Then, it signs the message and puts the corresponding sensor UUID in the JSON message.

Once the message is signed and transmitted through the socket to the file ‘aggregator.py’ on the aggregator side, the aggregator distributes the information packet to ‘rootcomputer.py’ for Merkle Root computation. The root is the method of validation in this implementation and is imperative to security. This is the item to be stored onto the Blockchain once validated with ‘validation.py’.

Finally, the data is stored into an SQL database through the python file ‘PyDbConn.py’. Connections to other databases can be initiated through the search variable ‘query’, where “Sensor_Data” is the new repository. A further development of the Database connection involves numbering the entries stored into the repository so the order of the Merkle Tree is preserved. Otherwise, shifting the data around causes the root of the tree to change, compromising data.

A quick explanation of all files is included here. To avoid redundancy, a more in-depth explanation is available within the files themselves.

Files on the Aggregator (Laptop):

Directory - /src aggregator.py - Main engine after enrollment, takes data through socket stream and bundles.

bridge_to_blockchain.py - Contains functions to simplify connection to smart contracts on blockchain. Redefines functions within contract_access.py.

contract_access.py - This file defines a class where a connection to our contract that is deployed on the blockchain. Defined here are methods that call and transact sending and retrieving data from this contract.

enrollment.py - Opens the enr.txt file that was passed via USB from the PI and grabs the public key and UUID. Once it has this information, it connects to a deployed contract and sends this data to the blockchain.

PyDbConn.py - Used to connect to the MS SQL database with functions to add entries and pull data.

requirements.txt - Compilation of the libraries used in the application for both the aggregator and the pi as well as their version numbers.

rootcomputer.txt - Contains one main function to compute the Merkle root from an input list of strings.

servermain.py - Uses Flask and an html template to host a webserver and display the two graphs created using matplotlib.

validation.py - Validates the data packet received using the public key stored upon enrollment.

static/main.js - Javascript template for Default Flask Server. templates/index.html - HTML template for Default Flask Server.

Files on the PI:

Directory - /pi socket_client.py - Retrieves data from the sensor and establishes a socket client with which to send data packets to the aggregator.

sign_data.py - Contains the logic for taking the data from the Arduino and packaging it into JSON with the UUID. Along with this it also signs the message using the sensor's private key.

sens_enroll.py - Used to create the private and public key as well as a sensor UUID, where the public key and sensor UUID will be written to a “enr.txt” file.

enr.txt - Contains the public key and sensor UUID that was created in sens_enroll.py.

requirements.txt - Compilation of libraries only used on the Pi.

.env - Contains the variables that have private information.

Directory - /pi/sensors/

arduino_sensor - Contains the class which holds the logic for grabbing the data from the Arduino by connecting to its serial comm connection port and cleaning / returning this data via a getter method.
