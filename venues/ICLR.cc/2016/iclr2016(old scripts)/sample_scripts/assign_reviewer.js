#!/usr/bin/env node

var fs = require('fs');
var request = require('request');

// The open review local url
var grpUrl = 'http://localhost:8529/_db/_system/openreview/groups';
var loginUrl = 'http://localhost:8529/_db/_system/openreview/login';

var headers = { 'User-Agent': 'test-create-script' };

//or3 request bodies
var userpass = {
  'id': 'ari@host.com',
  'password': ''
};

function or3post(url, body, headers) {
  this.url = url;
  this.method = 'POST';
  this.port = 80;
  this.json = true;
  this.body = body;
  this.headers = headers;
}

function callback(error, response, body) {
  if (!error && response.statusCode == 200) {
      console.log("SUCCESS");
      console.log(body);
  } else {
      console.log("ERROR: " + error);
      console.log("RESPONSE: " + response.statusCode);
  }
}

function loggedInHdr(token) {
  return {
  'Authorization': 'Bearer ' + token,
  'User-Agent': 'test-create-script'
  };
}

function revAssignment(papNum, revNum, rev) {
    return {
	'id': 'ICLR.cc/2016/-/workshop/paper/' + papNum + '/reviewer/' + revNum,
	'authors': ['ICLR.cc/2016'],
	'writers': ['ICLR.cc/2016'],
	'members': [rev],
	'signatories': ['ICLR.cc/2016/paper/' + papNum + '/reviewer/' + revNum],
	'readers': ['ICLR.cc/2016']
	//this.nonreaders = ICLR.cc/2016/belanger/conflicts
    };
}

function assign_rev(papNum, revNum, rev) {
    var loginReq = new or3post(loginUrl, userpass, headers);
    request(loginReq, function(error, response, body) {
	if (!error && response.statusCode == 200) {
            var token = body.token;
	    var assignment = revAssignment(papNum, revNum, rev);
	    var or3Assignment = new or3post(grpUrl, assignment, loggedInHdr(token));
	    request(or3Assignment, callback);
	}
    });
}

assign_rev(1,1,'ari@host.com');
