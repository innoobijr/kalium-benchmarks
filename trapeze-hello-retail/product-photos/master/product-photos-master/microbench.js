
/**
 * Handle the success of the process to obtain a photograph from a photographer
 * @param event The event indicating the context of the successful assignment
 * Example event:
 * {
 *   schema: 'com.nordstrom/retail-stream/1-0-0',
 *   origin: 'hello-retail/product-producer-automation',
 *   timeOrigin: '2017-01-12T18:29:25.171Z',
 *   data: {
 *     schema: 'com.nordstrom/product/create/1-0-0',
 *     id: 4579874,
 *     brand: 'POLO RALPH LAUREN',
 *     name: 'Polo Ralph Lauren 3-Pack Socks',
 *     description: 'PAGE:/s/polo-ralph-lauren-3-pack-socks/4579874',
 *     category: 'Socks for Men',
 *   }
 *   photographers: ['Erik'],
 *   photographer: {
 *     name: 'Erik',
 *     phone: '+<num>',
 *   },
 *   image: 'erik.hello-retail.biz/i/p/4579874',
 *   assignmentComplete: 'false'
 * }
 * @param context see Lambda docs
 * @param callback see Lambda docs
 */
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
const url = require('url');
const request = require('request-promise');
//const fetch = require('node-fetch');

function get_url() {
	return new Promise(function(resolve, reject) {
		request({
        		url: 'https://node0.controller.cs799-serverless-pg0.wisc.cloudlab.us:4443/image.jpg',
        		agentOptions: {
                		rejectUnauthorized: false
        		},
        		method: 'GET'
  		}, function (err, resp, body) {
        		//;console.log(body)
        		//const result = event.body;
        		resolve(resp)
 		 });
	});
}

module.exports = (event, context, callback) => {
  console.log(JSON.stringify(event));
  /*var res = event.body  
  request({
  	url: 'https://node0.controller.cs799-serverless-pg0.wisc.cloudlab.us:4443/image.jpg',
  	agentOptions: {
    		rejectUnauthorized: false
  	},
	method: 'GET'
  }, function (err, resp, body) {
 	//;console.log(body)
	//const result = event.body;
	callback(null, res)
  });*/
  //fetch('https://node0.controller.cs799-serverless-pg0.wisc.cloudlab.us:4443/image.jpg')
  //  .then(res => callback(null, event.body))
  //get_url().then(res => callback(null, event.body));
  request({
        url: 'https://node0.controller.cs799-serverless-pg0.wisc.cloudlab.us:4443/image.jpg',
        agentOptions: {
                rejectUnauthorized: false
        },
        method: 'GET'
  }, 'https://node0.controller.cs799-serverless-pg0.wisc.cloudlab.us:4443/image.jpg').then(res => {
	  callback(null, event.body)
  });
  
  //const result = event.body;
  //result.assignmentComplete = 'true';
  //result.photographer.status='complete'
  //callback(null, result)
};

