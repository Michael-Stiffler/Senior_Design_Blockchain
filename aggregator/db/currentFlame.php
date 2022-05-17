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
	$sql = "SELECT `Flame` FROM reports where Report_Time = (Select MAX(Report_Time) from reports)";
	$result = mysqli_query($dblink,$sql);
	
	$row = mysqli_fetch_assoc($result);
	echo $row['Flame'];
	
	mysqli_close($dblink);
?>
