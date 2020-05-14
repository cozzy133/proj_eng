function loadTemp() {
	var dataPoints = [];
	var chart = new CanvasJS.Chart("chartContainer", {
			title : {
				text : "Dynamic Data"
			},
			data : [{
					type : "spline",
					dataPoints : dataPoints
				}
			]
		});

	chart.render();

	var yVal = 0, updateCount = 0;
	var updateChart = function () {

		yVal = device.temp;
      	updateCount++;

		dataPoints.push({
			y : yVal
		});

        chart.options.title.text = "Temperature (Celcius)";
		chart.render();

	};

	// update chart every second
	setInterval(function(){updateChart()}, 1000);
}