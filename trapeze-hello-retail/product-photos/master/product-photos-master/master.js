"use strict"

const request = require('request-promise')

const constants = { 

      URL_ASSIGN: 'http://gateway.openfaas:8080/function/trapeze-product-photos-1-assign',
      URL_MESSAGE: 'http://gateway.openfaas:8080/function/trapeze-product-photos-2-message',
      URL_RECORD: 'http://gateway.openfaas:8080/function/trapeze-product-photos-2-record',
      URL_RECEIVE: 'http://gateway.openfaas:8080/function/trapeze-product-photos-3-receive',
      URL_SUCCESS: 'http://gateway.openfaas:8080/function/trapeze-product-photos-4-success',
      URL_REPORT: 'http://gateway.openfaas:8080/function/trapeze-product-photos-6-report',

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
       //console.log(constants.URL_ASSIGN);
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
	console.log(constants.URL_RECEIVE);
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
    if (event.path == '/request') {
      api.receiveRequest (event, context, callback);
    } else if (event.path == '/photos') {
      api.receivePhoto (event, context, callback);
    }
  
}
