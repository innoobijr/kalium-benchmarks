const shim = require('lambda-shim');

module.exports = (event, context, callback) => {
    var response = shim.makeShim( true);
    console.log('received response')
    console.log(response)
    response(event, context, callback)
}

/*const shim = require('lambda-shim'); // Ensure the correct path to lambda-shim.js
const fs = require("fs");
const conf = JSON.parse(fs.readFileSync('/home/app/function/conf.json', 'utf8')); // Ensure the correct path to your configuration file

module.exports = (event, context, callback) => {
    let reqUser;
    let reqPass;

    console.log(event);

    if (conf.runFromGET) { // Run http GET request on behalf of invoking user.
        console.log('In conf.runFromGET');

        // Extract user and pass from query parameters
        reqUser = event.queryStringParameters.user;
        reqPass = event.queryStringParameters.pass;

        if (conf.userPassForIFCOnly) {
            delete event.queryStringParameters.user;
            delete event.queryStringParameters.pass;
        }
    } else { // Run http POST request on behalf of invoking user.
        let reqBody;
        if (typeof event.body === "string") {
            reqBody = JSON.parse(event.body);
        } else {
            reqBody = event.body;
        }
        reqUser = reqBody.user;
        reqPass = reqBody.pass;
    }

    var response = shim.makeShim(true);
    response(event, context, callback, reqUser, reqPass);
};*/


