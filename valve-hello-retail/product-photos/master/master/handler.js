"use strict"

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
const request = require('request-promise');
const https = require('https');
const got = require('got');

const constants = { 

      URL_ASSIGN: process.env.URL_ASSIGN,
      URL_MESSAGE: process.env.URL_MESSAGE,
      URL_RECORD: process.env.URL_RECORD,
      URL_RECEIVE: process.env.URL_RECEIVE,
      URL_SUCCESS: process.env.URL_SUCCESS,
      URL_REPORT: process.env.URL_REPORT,

  };

const functions = {
    getRequestObject: (requestVals, url) => {
        return {
        method: 'POST',
        uri: url,
        body: requestVals,
        json: true
        }
    }
}

const api = {
    
    receiveRequest: (event, context, callback) => {
       console.log(constants.URL_ASSIGN);
        request(functions.getRequestObject(event.body, constants.URL_ASSIGN), constants.URL_ASSIGN)
            .then(res => {
                console.log('Assign result:');
                console.log(res);
                
                request(functions.getRequestObject(res, constants.URL_MESSAGE), constants.URL_MESSAGE)
                    .then(res => request(functions.getRequestObject(res, constants.URL_RECORD), constants.URL_RECORD))
                    .then(res => {
                        console.log('Final res')
                        console.log(res);
                        callback(null, res);
                    }
                        )
                    .catch(err =>{
                        console.log('err' + err)
                        callback(null, err)
                    });
                    
                
                
                    
            //         .then( res => {
            //             request(functions.getRequestObject(res, constants.))
            //                 .then(res => request(functions.getRequestObject(res, constants.URL_PUBLISH)))
            //                     .then(res => callback (null, res))
            //     }
            // )
            
            }
        )
    },

    receivePhoto: (event, context, callback) => {
        console.log('photoFunction')
        console.log(event.body)
        request(functions.getRequestObject(event.body, constants.URL_RECEIVE), constants.URL_RECEIVE)
            .then(res => {
                console.log('Result: ')
                console.log( res);
                request(functions.getRequestObject(res, constants.URL_SUCCESS), constants.URL_SUCCESS)
                .then(res => {
                    request(functions.getRequestObject(res, constants.URL_REPORT), constants.URL_REPORT)
                        .then(res => {
                            console.log('res');
                            console.log(res);
                            callback(null, res);
                        })
                        .catch(err =>{
                            console.log('err' + err)
                            callback(null, err)
                        });
                }    
            )
            }
        )
    }
}

module.exports = (event, context, callback) => {
    console.log('abcd')
    // Testing HTTPs proxying
    //request('https://node0.controller.cs799-serverless-pg0.wisc.cloudlab.us:4443/', function (error, response, body) {
  	//if (!error && response.statusCode == 200) {
    //		console.log(body);
  //	}
    //});
	/*var agentOptions;
	var agent;

	agentOptions = {
		host: 'node0.controller.cs799-serverless-pg0.wisc.cloudlab.us'
		, port: '4443'
		, path: '/'
		, rejectUnauthorized: false
	};

	agent = new https.Agent(agentOptions);

	request({
  		url: "https://node0.controller.cs799-serverless-pg0.wisc.cloudlab.us:4443/"
		, method: 'GET'
		, agent: agent
	}, function (err, resp, body) {
  		console.log(body)
	});

    //const got = require('got');
    got.get("https://node0.controller.cs799-serverless-pg0.wisc.cloudlab.us:4443/", { encoding: 'utf-8' }).then(
      res =>
	    console.log(res.body)
    )*/

    if (event.path == '/request') {
      api.receiveRequest (event, context, callback);
    } else if (event.path == '/photos') {
      api.receivePhoto (event, context, callback);
    }
  
}
