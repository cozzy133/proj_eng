function loadPressure() {
	var dataPoints = [];
	var chart = new CanvasJS.Chart("chartContainer1", {
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

		yVal = device.pressure;
      	updateCount++;

		dataPoints.push({
			y : yVal
		});

        chart.options.title.text = "Pressure (Pa)";
		chart.render();

	};

	// update chart every second
	setInterval(function(){updateChart()}, 1000);
}