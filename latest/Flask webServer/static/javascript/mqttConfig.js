// Create a client instance
  client = new Paho.MQTT.Client("hairdresser.cloudmqtt.com", 37043, "web_" + parseInt(Math.random() * 100, 10));

  var device = {
    temp: 0,
    pressure: 0,
    altitude: 0,
    distance: 0
}

  // set callback handlers
  client.onConnectionLost = onConnectionLost;
  client.onMessageArrived = onMessageArrived;
  var options = {
    useSSL: true,
    userName: "cmszpdkk",
    password: "Z0_OVJO9x11Z",
    onSuccess:onConnect,
    onFailure:doFail
  }

  // connect the client
  client.connect(options);

  // called when the client connects
  function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
    client.subscribe("/fyp/temp");
    client.subscribe("/fyp/altitude");
    client.subscribe("/fyp/pressure");
    client.subscribe("/fyp/obstacle");
    message = new Paho.MQTT.Message("Hello CloudMQTT");
    message.destinationName = "/cloudmqtt";
    loadTemp();
    loadAlt();
    loadPressure();
    client.send(message);
  }

  function doFail(e){
    console.log(e);
  }

  // called when the client loses its connection
  function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
      console.log("onConnectionLost:"+responseObject.errorMessage);
    }
  }

  // called when a message arrives
  function onMessageArrived(message) {
    console.log("onMessageArrived:"+message.payloadString);
    console.log("Topic:     " + message.destinationName);
    if (message.destinationName === "/fyp/temp") {
        device.temp=parseFloat(message.payloadString);
    } else if (message.destinationName === "/fyp/altitude") {
        device.altitude=parseFloat(message.payloadString);
    } else if (message.destinationName === "/fyp/pressure") {
        device.pressure=parseFloat(message.payloadString);
    } else if (message.destinationName === "/fyp/obstacle") {
        if (parseFloat(message.payloadString) === 1.0) {
            device.distance=parseFloat(message.payloadString);
            document.getElementById('myImage').src='static\\images\\not-clear.png';
        } else {
            device.distance=parseFloat(message.payloadString);
            document.getElementById('myImage').src='static\\images\\clear.png';
        }
    } else {
        console.log("other topic")
    }
  }