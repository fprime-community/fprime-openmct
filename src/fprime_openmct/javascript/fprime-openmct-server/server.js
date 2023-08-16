/**
 * Basic implementation of a history and realtime server.
 */

var FPrimeTelemListener = require('./fprime-telem-listener');
var RealtimeServer = require('./realtime-server');
var HistoryServer = require('./history-server');
var StaticServer = require('./static-server');

var expressWs = require('express-ws');
var app = require('express')();
expressWs(app);

var fprimeListener = new FPrimeTelemListener();
var realtimeServer = new RealtimeServer(fprimeListener);
var historyServer = new HistoryServer(fprimeListener);
var staticServer = new StaticServer();

app.use('/realtime', realtimeServer);
app.use('/history', historyServer);
app.use('/', staticServer);

var port = process.env.PORT || 8080

app.listen(port, function () {
    console.log('Open MCT hosted at http://localhost:' + port);
    console.log('History hosted at http://localhost:' + port + '/history');
    console.log('Realtime hosted at ws://localhost:' + port + '/realtime');
});
