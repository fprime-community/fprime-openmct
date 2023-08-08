/*
 fprime-telem-listener.js listens to F-Prime Telemetry on a Server and Formats it into OpenMCT Telemetry
*/
var express = require('express');
var bodyParser = require('body-parser');

var app = express();
var fs = require('fs');

//Get Initial Telemetry States from data.json
var state = JSON.parse(fs.readFileSync('initial_states.json', 'utf8'));
//console.log(state);


app.use(bodyParser.json({limit: '500mb'}));
app.use(bodyParser.urlencoded({ extended: false }));

// Server listening to PORT 4052
app.listen(4052);

/**
 *  Sets up State Object for Tracking FPrime Telemetry
 *  Polls upstateState and generateTelemetry at 1 Hz
 */
function FPrimeTelemListener() {
    this.state = state;
    //console.log(state);
    this.state["comms.recd"] = 0;
    this.state["comms.sent"] = 0;
    this.history = {};
    this.listeners = [];
    Object.keys(this.state).forEach(function (k) {
        this.history[k] = [];
    }, this);

    setInterval(function () {
        this.updateState();
        this.generateTelemetry();
    }.bind(this), 1000);

};

/**
 *  Listen for FPrime Telemetry from the Specified IP and Port
 *  Update State Object based on most recent FPrime Telemetry from each State Entry
 */
FPrimeTelemListener.prototype.updateState = function () {

    app.post("/fprime_telem", (req, res) => {

        var i = 0;
        //Process each telemetry entry in a request
        while (i < req.body.telem.length)
        {
            try {
                //Check that the state key matches the recieved name
                const name = req.body.telem[i].name;
                //console.log(name);
                for (const [ key, value ] of Object.entries(this.state)) {
                        if (key == name) {
                            //console.log("processing");
                            //Assign State entries to the recieved data values 
                            this.state[key] = req.body.telem[i].data.val;
                            //console.log(this.state[key]);
                        }
                }     
            } catch (error) {
                console.log(error);
            }
        
        i = i+1;   
        }
        // Return json response
        res.json({ result: 'done' });
    });
    
};

/**
 *  Sets up communication between State Object and OpenMCT Telemetry 
 */
FPrimeTelemListener.prototype.generateTelemetry = function () {
    var timestamp = Date.now(), sent = 0;
    Object.keys(this.state).forEach(function (id) {
        var state = { timestamp: timestamp, value: this.state[id], id: id};
        this.notify(state);
        this.history[id].push(state);
        this.state["comms.sent"] += JSON.stringify(state).length;
    }, this);
};

FPrimeTelemListener.prototype.notify = function (point) {
    this.listeners.forEach(function (l) {
        l(point);
    });
};

FPrimeTelemListener.prototype.listen = function (listener) {
    this.listeners.push(listener);
    return function () {
        this.listeners = this.listeners.filter(function (l) {
            return l !== listener;
        });
    }.bind(this);
};

module.exports = function () {
    return new FPrimeTelemListener()
};