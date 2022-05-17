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
	$sql = "SELECT * FROM Sensor_Data where Time = (Select MAX(Time) from Sensor_Data)";
	$result = mysqli_query($dblink,$sql);
	$row = mysqli_fetch_assoc($result);

	mysqli_close($dblink);
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sensor Dashboard</title>
    <!-- Bootstrap -->
   <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
	  	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
		<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
		<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
		<link rel="stylesheet" href="/resources/demos/style.css">
	<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
	  <script type="text/javascript">

  // Load the Visualization API and the controls package.
  // Packages for all the other charts you need will be loaded
  // automatically by the system.
		google.charts.load('current', {'packages':['gauge', 'corechart', 'controls', 'table']});
    google.charts.setOnLoadCallback(drawHumid);
		google.charts.setOnLoadCallback(drawCurrent);
		google.charts.setOnLoadCallback(drawPress);
		google.charts.setOnLoadCallback(drawResistance);
		function drawTempTable() {
		google.charts.setOnLoadCallback(drawTempDashboard);
		}
		function drawPressTable() {
		google.charts.setOnLoadCallback(drawPressDashboard);
		}
		function drawHumidTable() {
		google.charts.setOnLoadCallback(drawHumidDashboard);
		}
		function drawResistTable() {
		google.charts.setOnLoadCallback(drawResistDashboard);
		}
		 $(document).ready(function(){
			  $.get("currentVibration.php", function(data){
				  $("#vib_div2").html(data);
			  });

		  });


      function drawCurrent() {
			var currentTemp = google.visualization.arrayToDataTable([
				   ['Label', 'Value'],
          		   ['Temperature', <?php echo $row['Temperature']]
			]);
        	 var options = {
          			width: '80%', height: 200,
          			redFrom: 30, redTo: 50,
          			yellowFrom:25, yellowTo: 30,
          			minorTicks: 5,
		  			max: 50
        		   };

        	var tempChart = new google.visualization.Gauge(document.getElementById('temp_div2'));

			tempChart.draw(currentTemp, options);
		  	$.ajax({
                url: 'currentTemp.php',
                type: 'get',
				dataType: 'JSON',
                success: function(response){
				   console.log(JSON.stringify(response));
				   currentTemp.setValue(0, 1, response);
                   tempChart.draw(currentTemp, options);
				}
			});
      }
      function drawPress() {

        var press = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Pressure', 0]
        ]);

        var options = {
          width: '80%', height: 200,
          redFrom: 0, redTo: 50,
		yellowColor:'#e2431e',
          yellowFrom:150, yellowTo: 200,
          minorTicks: 10,
			max: 200
        };

        var chart = new google.visualization.Gauge(document.getElementById('press_div2'));

        chart.draw(press, options);
		$.ajax({
                url: 'currentPress.php',
                type: 'get',
				dataType: 'JSON',
                success: function(response){
				   console.log(JSON.stringify(response));
				   press.setValue(0, 1, response);
                   chart.draw(press, options);
				}
			});

      }
	  function drawHumid() {

        var humid = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humidity', 0]
        ]);

        var options = {
          width: '80%', height: 200,
          redFrom: 80, redTo: 100,
          yellowFrom:65, yellowTo: 80,
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('humid_div2'));

        chart.draw(humid, options);
		$.ajax({
                url: 'currentHumid.php',
                type: 'get',
				dataType: 'JSON',
                success: function(response){
				   console.log(JSON.stringify(response));
				   humid.setValue(0, 1, response);
                   chart.draw(humid, options);
				}
			});


      }
		function drawResistance() {

        var resist = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Resistance', 0]
        ]);

        var options = {
          width: '80%', height: 200,
          redFrom: 0, redTo: 50000,
          yellowFrom:50000, yellowTo: 100000,
          minorTicks: 5,
		  max: 500000
        };

        var chart = new google.visualization.Gauge(document.getElementById('resist_div2'));

        chart.draw(resist, options);
		$.ajax({
                url: 'currentResist.php',
                type: 'get',
				dataType: 'JSON',
                success: function(response){
				   console.log(JSON.stringify(response));
				   resist.setValue(0, 1, response);
                   chart.draw(resist, options);
				}
			});

      }
	function drawTempDashboard() {
            $.ajax({
                url: 'newTempData.php',
                type: 'get',
                dataType: 'JSON',
                success: function(response){
				   console.log(response);
                   var tempData = new google.visualization.DataTable(response);
                   var options = {
                    	title: 'Temperature over Time',
                    	width:'100%',
                   		height: '25%',
					    explorer: { axis: 'horizontal' },
                    	legend: { position: 'bottom' }
                    };

                    var lineChart = new google.visualization.LineChart(document.getElementById('chart_div'));

                   	lineChart.draw(tempData, options);

                    var table = new google.visualization.Table(document.getElementById('table_div'));

                   table.draw(tempData, {showRowNumber: true, width: '100%', height: '100%'});
                }
           });
        }
		function drawPressDashboard() {
            $.ajax({
                url: 'newPressData.php',
                type: 'get',
                dataType: 'JSON',
                success: function(response){
				   console.log(response);
                   var pressData = new google.visualization.DataTable(response);
                   var options = {
                    	title: 'Pressure over Time',
                    	width:'100%',
                   		height: '25%',
					    explorer: { axis: 'horizontal' },
                    	legend: { position: 'bottom' }
                    };

                    var lineChart = new google.visualization.LineChart(document.getElementById('chart_div'));

                   	lineChart.draw(pressData, options);

                    var table = new google.visualization.Table(document.getElementById('table_div'));

                   table.draw(pressData, {showRowNumber: true, width: '100%', height: '100%'});
                }
           });
        }
		function drawHumidDashboard() {
            $.ajax({
                url: 'newHumidData.php',
                type: 'get',
                dataType: 'JSON',
                success: function(response){
				   console.log(response);
                   var humidData = new google.visualization.DataTable(response);
                   var options = {
                    	title: 'Humidity over Time',
                    	width:'100%',
                   		height: '25%',
					    explorer: { axis: 'horizontal' },
                    	legend: { position: 'bottom' }
                    };

                    var lineChart = new google.visualization.LineChart(document.getElementById('chart_div'));

                   	lineChart.draw(humidData, options);

                    var table = new google.visualization.Table(document.getElementById('table_div'));

                   table.draw(humidData, {showRowNumber: true, width: '100%', height: '100%'});
                }
           });
        }
		function drawResistDashboard() {
            $.ajax({
                url: 'newResistData.php',
                type: 'get',
                dataType: 'html',
                success: function(response){
				   console.log(response);
                   var resistData = new google.visualization.DataTable(response);
                   var options = {
                    	title: 'Gas Resistance over Time',
                    	width:'100%',
                   		height: '25%',
					    explorer: { axis: 'horizontal' },
                    	legend: { position: 'bottom' }
                    };

                    var lineChart = new google.visualization.LineChart(document.getElementById('chart_div'));

                   	lineChart.draw(resistData, options);

                    var table = new google.visualization.Table(document.getElementById('table_div'));

                   table.draw(resistData, {showRowNumber: true, width: '100%', height: '100%'});
                }
           });
        }
    </script>
  </head>

  <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-success">
      <a class="navbar-brand" href="index.html">Dashboard&nbsp;</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="index.html">Home <span class="sr-only">current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="sensor1_dashboard.html">Sensor 1<span class="sr-only">current)</span></a>
          </li>
		  <li class="nav-item">
            <a class="nav-link" href="#">Sensor 2<span class="sr-only">current)</span></a>
		  </li>
		  <li class="nav-item">
            <a class="nav-link" href="#">Sensor 3<span class="sr-only">current)</span></a>
		  </li>
        </ul>
</div>
	  </nav>
<section>
	<div class="container" id="sensor_information" align="center" style="font-size: 28px; font-weight: bold">Sensor 1
	</div>
	<div id="alert_div" align="center" style="font-size: 34px; font-weight: bold; color: darkred;"></div>
</section>
<section>
  <div class="container">
        <div class="row">
          <div id="temp_div" class="col-lg-4 col-md-6 col-12" align="center"><a href="#" onclick="drawTempTable()">Temperature (C)</a>
			  <div id="temp_div2"></div>
          </div>
          <div id="press_div" class="col-lg-4 col-md-6 col-12" align="center"><a href="#" onclick="drawPressTable()">Pressure (kPa)</a>
			<div id="press_div2"></div>
		  </div>
          <div id="humid_div" class="col-lg-4 d-md-none d-lg-block" align="center"><a href="#" onclick="drawHumidTable()">Humidity (%)</a>
			<div id="humid_div2"></div>
		  </div>
		   <div id="resist_div" class="col-lg-4 col-md-6 col-12" align="center"><a href="#" onclick="drawResistTable()">Gas Resistance (Ohms)</a>
			<div id="resist_div2"></div>
		  </div>
          <div id="aqi_div" class="col-lg-4 col-md-6 col-12" align="center">AQI Level (0-500)
			  <div id="aqi_num" style="font-size: 38px; font-weight: bold"></div>
			  <div id="aqi_text" style="font-size: 38px; background-color: yellow; font-weight: bold"></div>
		  </div>
          <div id="vib_div" align="center" class="col-lg-4 d-md-none d-lg-block">Vibration (G)
			<div id="vib_div2" style="font-size: 24px; font-weight: bold"></div>
		  </div>
    </div>
      </div>
    </section>

	<hr>
	<section>
    <div id="report_container" align="center">
	    <div class="row">
          <div id="control_div" class="col-lg-4 col-md-6 col-12 offset-xl-1 col-xl-5" align="center">
			  <div id="chart_div" height="200px">
			  </div>
			  <div id="controller_div"></div>
			</div>
          <div id="table_div" class="col-lg-4 col-md-6 col-12 offset-xl-0 col-xl-5" align="center">
		  </div>
		</div>
	</div>
	</section>
    <hr>
<footer class="text-center">
  <div class="container2">
        <div class="row">
          <div class="col-12">
            <p>Copyright © Cleveland State University</p>
          </div>
        </div>
      </div>
    </footer>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="file:///C|/wamp64/www/sensor/js/jquery-3.4.1.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/popper.min.js"></script>
    <script src="js/bootstrap-4.4.1.js"></script>
  </body>
</html>
