
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
    '314357337812-0569sb35jc4vpq8gqihrlk5kkl3e2bie.apps.googleusercontent.com';

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
};

/**
 * Loads the application UI after the user has completed auth.
 */
rateit.server.userAuthed = function() {
  gapi.client.oauth2.userinfo.get().execute(function(resp) {
    if (!resp.code) {
      rateit.server.signedIn = true;
    }
  });
};


/**
 * Presents the user with the authorization popup.
 */
rateit.server.auth = function(callback_success, callback_fail) {
  if (!rateit.server.signedIn) {
    var userinfoFunc = function(resp) {
      if (!resp.code) {
        rateit.server.signedIn = true;
        callback_success();
      } else {
        callback_fail();
      }
    }

    var signinFunc = function() {
        gapi.client.oauth2.userinfo.get().execute(userinfoFunc);
    };

    rateit.server.signin(false, signinFunc);
  } else {
    callback_success();
  }
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
      rateit.client.init();
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

/** rateit.client global namespace. */
rateit.client = rateit.client || {};

/** Set the current view to display */
rateit.client.set_current_view = function(view_name) {
  var list = rateit.pages.list;
  var page = undefined;
  for (var i = 0; i < list.length; ++i) {
    if (list[i].tag === view_name) {
      page = list[i];
      continue;
    }
    $(list[i].tag).hide();
  }

  var success_func = function() {
    $(view_name).show();
    rateit.current_page = view_name;
  };

  if (page && page.preload_func) {
    var fail_func = function() {
      $(page.fail_tag).show();
      rateit.current_page = page.fail_tag;
    };
    
    page.preload_func(success_func, fail_func);
  } else {
    success_func();
  }
}

/** A pre-auth function. */

rateit.client.preauth = function(success_func, fail_func) {
};

/** Initialize the client */

rateit.client.init = function() {
  rateit.client.set_current_view(rateit.current_page);

  $("#rate_trip_form").submit(function(event) {
    rateit.client.submit_rating();
    event.preventDefault();
  });

  $("#rateit-func-create_alert").submit(function(event) {
    alert("TODO need submit alert function");
    event.preventDefault();
  });
  
  rateit.client.initplugin();
}

rateit.client.report_error = function(response) {
    alert("Error code = " + responsue.code);
}

rateit.server.sumbit_trip_rating = function(values) {
  var request = {
      'route_id' : values.route_id, 
      'is_service_ontime' : values.is_service_ontime,
      'is_service_clean' : values.is_service_clean,
      'crowdedness' : values.crowdedness,
      'comfort_rating' : values.comfort_rating,
      'driver_rating' : values.driver_rating
    };
    
  if (values.comments) {
    request['comments'] = values.comments;
  }
  
  gapi.client.rateit.trip_rating.submit(request).execute(function(resp) {
      if (resp.code) {
          // There was an error
          rateit.client.report_error(resp);
      } else {
          // Clear form
          $('#rate_trip_form').clear();
      }
  });
};

rateit.client.map_values = function(mapping, values) {
    var result = {};
    for (var i = 0; i < values.length; ++i) {
        var value = values[i];
        var map = mapping[value.name];
        result[map.id] = map.func(value.value);
    }
    return result;
}

rateit.client.pass = function(value) {
    return value;
}

rateit.client.bool = function(value) {
    return value === "T";
}

rateit.client.submit_rating_mapping = {
    'inputRouteId3' : { id: 'route_id', func: rateit.client.pass },
    'inputServiceOnTime3' : { id: 'is_service_ontime', func: rateit.client.bool },
    'inputServiceClean3' : { id: 'is_service_clean', func: rateit.client.bool },
    'inputServiceCrowded3' : { id: 'crowdedness', func: rateit.client.pass },
    'inputServiceComfort3' : { id: 'comfort_rating', func: rateit.client.pass },
    'inputDriverPoliteness3' : { id: 'driver_rating', func: rateit.client.pass },
    'inputComments3' : { id: 'comments', func: rateit.client.pass }
};

rateit.client.submit_rating = function() {
  rateit.client.set_current_view("#rateit-func-rate-trip-response");
  var values = rateit.client.map_values(
      rateit.client.submit_rating_mapping, 
      $("#rate_trip_form").serializeArray());
  
  rateit.server.sumbit_trip_rating(values);
}

// JQuery plugin to clear form, from Francis Lewis on stackoverflow.
rateit.client.initplugin = function() {

  $.fn.clear = function()
  {
    var $form = $(this);

    $form.find('input:text, input:password, input:file, textarea').val('');
    $form.find('select option:selected').removeAttr('selected');
    $form.find('input:checkbox, input:radio').removeAttr('checked');
    $form.find('label').removeClass('active');

    return this;
  }; 
};

rateit.pages = rateit.pages || {};

rateit.pages.list = rateit.pages.list || [];

/**
 * Adds a page to the list of pages.
 */
rateit.pages.add = function(tag, preload_func, fail_tag) {
  if (!fail_tag) {
    fail_tag = "#rateit-func-login-fail-message";
  }
  rateit.pages.list.push({
    'tag': tag,
    'fail_tag' : fail_tag,
    'preload_func': preload_func
    });
};

rateit.current_page = "#rateit-func-sign-in";



