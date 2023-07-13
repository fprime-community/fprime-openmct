/*
 Spacecraft.js simulates a small spacecraft generating telemetry.
*/
var express = require('express');
var bodyParser = require('body-parser');

var app = express();
var fs = require('fs');
var state = JSON.parse(fs.readFileSync('../data.json', 'utf8'));
console.log(state);


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// Server listening to PORT 4052
app.listen(4052);

function Heli() {
    this.state = state;
    console.log(state);
    this.state["comms.recd"] = 0;
    this.state["comms.sent"] = 0;
    //{
    //    "mpptTester.PvAdcDn": 0,
    //    "mpptTester.PiAdcDn": 0,
    //    "mpptTester.BvAdcDn": 0,
    //    "mpptTester.BiAdcDn": 0,
    //    "comms.recd": 0,
    //    "comms.sent": 0,
    //};
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

Heli.prototype.updateState = function () {

    app.post("/helitelem", (req, res) => {
  
        var i = 0;
        for (const [ key, value ] of Object.entries(this.state)) {
            //Check that the state key matches the recieved name
            const name = req.body.telem[i].name;
            console.log(name);
            if (key == name) {
                console.log("processing");
                //Assign State entries to the recieved data values 
                this.state[key] = req.body.telem[i].data.val;
                console.log(this.state[key]);
            }
            i = i+1;
        }

        // Retrieve array form post body
        //this.state["mpptTester.PvAdcDn"] = Number(req.body.telem[0].data.val);  
        //this.state["mpptTester.PiAdcDn"] = req.body.telem[1].data.val;  
        //this.state["mpptTester.BvAdcDn"] = req.body.telem[2].data.val;  
        //this.state["mpptTester.BiAdcDn"] = req.body.telem[3].data.val;  
        //var val = req.body.val;
        //var time = req.body.time;
        //console.log('PV Counts: ' + this.state["mpptTester.PvAdcDn"]);
        //console.log('Val ' + val);
        //console.log('Time ' + time);
    
     
        //console.log(sum);
      
        // Return json response
        res.json({ result: 'done' });
    });
    
};

/**
 * Takes a measurement of spacecraft state, stores in history, and notifies 
 * listeners.
 */
Heli.prototype.generateTelemetry = function () {
    var timestamp = Date.now(), sent = 0;
    Object.keys(this.state).forEach(function (id) {
        var state = { timestamp: timestamp, value: this.state[id], id: id};
        this.notify(state);
        this.history[id].push(state);
        this.state["comms.sent"] += JSON.stringify(state).length;
    }, this);
};

Heli.prototype.notify = function (point) {
    this.listeners.forEach(function (l) {
        l(point);
    });
};

Heli.prototype.listen = function (listener) {
    this.listeners.push(listener);
    return function () {
        this.listeners = this.listeners.filter(function (l) {
            return l !== listener;
        });
    }.bind(this);
};

module.exports = function () {
    return new Heli()
};