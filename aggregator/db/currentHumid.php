<?php

include("config.php");

//Create database connection
	$dblink = new mysqli($dbhost, $dbuser, $dbpass, $dbname);

//Check connection was successful
	if ($dblink->connect_errno) {
		printf("Failed to connect to database");
		exit();
	}

# Grab the data from the database
	$sql = "SELECT Humidity FROM Sensor_Data where Time = (Select MAX(Time) from Sensor_Data)";
	$result = mysqli_query($dblink,$sql);

	$row = mysqli_fetch_assoc($result);
	echo $row['Humidity'];
	mysqli_close($dblink);
?>
