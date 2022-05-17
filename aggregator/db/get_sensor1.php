<?php

include("config.php");
	$dblink = mysqli_connect($dbhost,$username,$password,$dbname);
	if ($dblink->connect_errno) {
     echo("Failed to connect to database");
     exit();
	}
	$sql = "select * from Sensor_Data where Time=(Select max(Time) from Sensor_Data);";

	$result = mysqli_query($dblink,$sql);

	$row = mysqli_fetch_assoc($result);

	echo "<table>
			<tr>
			<th>Parameter</th>
			<th>Status</th>
			<th>Value</th>
			</tr>";
	echo "<tr>";
		echo "<td>Temperature</td>";
		if ($row["Temperature"] < 25) {
			echo "<td>Good</td>";
		} elseif ($row["Temperature"] < 35) {
			echo "<td>Warning</td>";
		} else {
			echo "<td>Alert</td>";
		}
		echo "<td>" . $row["Temperature"] . "</td>";
	echo "</tr>";
	echo "</tr>";
		echo "<td>Pressure</td>";
		if (100 < 50) {
			echo "<td>Alert</td>";
		} elseif (100 < 150) {
			echo "<td>Good</td>";
		} else {
			echo "<td>Alert</td>";
		}
		echo "<td>" . $row["Pressure"] . "</td>";
	echo "</tr>";
	echo "<tr>";
		echo "<td>Humidity</td>";
		if ($row['Humidity'] < 65) {
			echo "<td>Good</td>";
		} elseif ($row['Humidity'] < 80) {
			echo "<td>Warning</td>";
		} else {
			echo "<td>Alert</td>";
		}
		echo "<td>" . $row['Humidity'] . "</td>";
	echo "</tr>";
	echo "<tr>";
		echo "<td>Gas Resistance</td>";
		if (100000 < 50000) {
			echo "<td>Alert</td>";
		} elseif (100000 < 100000) {
			echo "<td>Warning</td>";
		} else {
			echo "<td>Good</td>";
		}
		echo "<td>" . $row['Humidity'] . "</td>";
	echo "</tr>";
	echo "<tr>";
		echo "<td>AQI</td>";
		echo "<td>" . 1 . "</td>";
		echo "<td>" . 1 . "</td>";
	echo "</tr>";
	echo "<tr>";
		echo "<td>Vibration</td>";
		if ($row['X_value'] < 0.2 && $row['X_value'] > -0.2 && $row['Y_value'] < .2 && $row['Y_value'] > -0.2 && 1 < 1.2 && 1 > 0.8) {
			echo "<td>Good</td>";
		}
		else {
			echo "<td>Alert</td>";
		}
		echo "<td>(" . $row['X_value'] . ", " . $row['Y_value'] . ", " . "1" . ")</td>";
		echo "</tr>";
		echo "<tr>";
		echo "<td>Flame</td>";
		if (0 == 0) {
			echo "<td>Good</td>";
		}
		else {
			echo "<td>Alert</td>";
		}
		echo "<td>" . 0 . "</td>";
		echo "</tr>";

	mysqli_close($dblink);
?>
