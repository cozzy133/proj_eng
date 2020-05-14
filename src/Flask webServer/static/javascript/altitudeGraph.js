function loadAlt() {
	var dataPoints = [];
	var chart = new CanvasJS.Chart("chartContainer2", {
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

		yVal = device.altitude;
      	updateCount++;

		dataPoints.push({
			y : yVal
		});

        chart.options.title.text = "Altitude (m)";
		chart.render();

	};

	// update chart every second
	setInterval(function(){updateChart()}, 1000);
}