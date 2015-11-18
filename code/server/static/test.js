
/** rateit global namespace for rateit projects. */
var rateit = rateit || {};

/** rateit.server global namespace. */
rateit.server = rateit.server || {};

rateit.server.signedIn = false;

/**
 * Client ID of the application (from the APIs Console).
 * @type {string}
 */
rateit.server.CLIENT_ID =
    'rateit-bus-web';

/**
 * Scopes used by the application.
 * @type {string}
 */
rateit.server.SCOPES =
    'https://www.googleapis.com/auth/userinfo.email';

/**
 * Handles the auth flow, with the given value for immediate mode.
 * @param {boolean} mode Whether or not to use immediate mode.
 * @param {Function} callback Callback to call on completion.
 */
rateit.server.signin = function(mode, callback) {
  gapi.auth.authorize({
      client_id: rateit.server.CLIENT_ID,
      scope: rateit.server.SCOPES,
      immediate: mode
    },
    callback);

  rateit.server.testapi();
};

rateit.server.testapi = function() {
  gapi.client.rateit.issue.report({
      'route_id': '617X',
      'stop_id': 'Meurants Ln',
      'report_date_time': new Date(),
      'gps_location': {
        'latitude' : 25.0,
        'longitude' : 35.0
      },
      'rating_type': 'LATE',
    }).execute(function(resp) {
      if (!resp.code) {
        alert(resp.responseText);
      } else {
        alert('issue.report error: ' + resp.code);
      }
      rateit.server.test2api();
    });
};

rateit.server.test2api = function() {
  var rid = '616X'
  gapi.client.rateit.aggregate_route_rating.get({
      'route_id': rid,
    }).execute(function(resp) {
      if (!resp.code) {
        if (resp.is_success) {
          alert("got " + rid + " aggregate route data.");
        } else {
          alert("get failed: " + resp.status_message);
        }
      } else {
        alert('aggregate_route_rating.get error: ' + resp.code);
      }
    });
};


/**
 * Loads the application UI after the user has completed auth.
 */
rateit.server.userAuthed = function() {
  alert("userAuthed");
  var request = gapi.client.oauth2.userinfo.get().execute(function(resp) {
    rateit.server.testapi();
    if (!resp.code) {
      rateit.server.signedIn = true;
    }
  });
};


/**
 * Initializes the enpoints apis.
 */
rateit.server.init = function(apiRoot) {

  // Loads the OAuth and rateit APIs asynchronously.
  var apisToLoad;
  var callback = function() {
    if (--apisToLoad == 0) {
      // Start the application.
      rateit.server.signin(true, rateit.server.userAuthed);
    }
  }
  var clients_to_load = [
    ['rateit', 'v1', callback, apiRoot],
    ['oauth2', 'v2', callback, undefined],
  ];

  apisToLoad = clients_to_load.length;

  for (var i = 0; i < clients_to_load.length; ++i) {
    var args = clients_to_load[i];
    gapi.client.load(args[0], args[1], args[2], args[3]);
  }
};

