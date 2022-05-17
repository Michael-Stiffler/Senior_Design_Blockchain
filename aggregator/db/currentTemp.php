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
	$sql = "SELECT TOP 1 Temperature FROM Sensor_Data ORDER BY Time Desc";
	$result = mysqli_query($dblink,$sql);

	$row = mysqli_fetch_assoc($result);
	echo $row['Temperature'];
	mysqli_close($dblink);
?>
