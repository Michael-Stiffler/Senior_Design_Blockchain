<?php
        include("config.php");
        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
        }
        $dir    = "/home/appmngr/sample";
        $files1 = scandir($dir, SCANDIR_SORT_DESCENDING);
        foreach($files1 as $files){
                $loadData = file_get_contents($dir . "/" . $files);
                $data = json_decode($loadData, true);
				$ret = str_replace(".json", "", $files);
                list($year, $month, $day, $time) = explode("-", $ret);
                list($hour, $minute, $second) = explode("_", $time);
                $d = "$year-$month-$day $hour:$minute:$second";
				$array = [];
                foreach($data['datapoints'] as $point){
                        $value = $point['Datapoint'];
						$newArray = array($value);
						array_push($array, $newArray);
                };
                $sql = "INSERT INTO reports (Report_Time, Temperature, Pressure, Humidity, `Gas Resistance`, AQI, `AQI Level`, Flame, `X Vibration`, `Y Vibration`, `Z Vibration`) VALUES ('$d', $array[0], $array[1], $array[2], $array[3], $array[4], '$array[5]', $array[6], $array[7], $array[8], $array[9])";
                if(mysqli_query($conn, $sql)){
                    echo "Records inserted successfully.";
                } else{
                    echo "ERROR: Could not able to execute $sql. " . mysqli_error($conn);
                }
		};

        $conn->close();
?>
