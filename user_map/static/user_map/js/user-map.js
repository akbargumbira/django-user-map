/**
 * Author: Akbar Gumbira (akbargumbira@gmail.com)
 * Description:
 * This file contains methods related directly to user map.
 * It follows Airbnb Javascript style guide (https://github.com/airbnb/javascript)
 * and JSDoc for the documentation.
 */

/**
 * Add users to the respective layer based on role.
 * @param {string} url The url view to get users.
 * @param {object} users_layer Passed users' layer
 * @param {object} icon The icon object for marker
 * @name L The Class from Leaflet.
 * @property geoJson Property of L class.
 * @property users Property of response object.
 * @function addTo add child element to the map.
 * @property properties Property of a feature.
 * @property popup_content property of properties.
 * @function bindPopup Bind popup to marker
 */
function addUsers(url, users_layer, icon) {
  $.ajax({
    type: 'GET',
    url: url,
    dataType: 'json',
    success: function (response) {
       L.geoJson(response, {
         onEachFeature: function (feature, layer) {
           var feature_roles = [];
           for (i = 0; i < feature.properties.roles.length; ++i){
             feature_roles.push(roles_dict[feature.properties.roles[i]]);
           }
           var data = {
             properties: feature.properties,
             roles: feature_roles
           };
           var popup_content = popup_template.render(data);
           layer.bindPopup(popup_content);
         },
         pointToLayer: function(feature, latlng) {
           return L.marker(latlng, {icon: icon})
         }
       }).addTo(users_layer);

      filterUsers();
    }
  });
}

/**
 * Filter users based on the filter control
 */
function filterUsers() {
  // Clear previous displayed_users
  displayed_users.clearLayers();

  // Get all selected roles
  var checked_roles = [];
  $("input:checkbox[class=role-filter]:checked").each(function () {
        checked_roles.push($(this).val());
  });

  users_layer.eachLayer(function(layer) {
    for (var i = 0; i < checked_roles.length; i++) {
      if (layer.feature.properties.roles.indexOf(parseInt(checked_roles[i])) !== -1) {
        displayed_users.addLayer(layer);
        break;
      }
    }
  });
}

/**
 * Create Data Privacy Control instance on the bottom left of the map.
 * @property Control
 * @property DomUtil
 * @property DomEvent
 * @returns {object} control
 */
function createDataPrivacyControl() {
  var control;
  control = L.Control.extend({
    options: {
      position: 'bottomleft'
    },
    onAdd: function () {
      var data_privacy_container = L.DomUtil.create('div',
          'leaflet-control-attribution');
      var data_privacy_title = "Data Privacy";
      var data_privacy_content = $( "#data-privacy-content-section" ).html();
      onDataPrivacyClick = function () {
        showInformationModal(data_privacy_title, data_privacy_content);
      };
      data_privacy_container.innerHTML += "<a onclick='onDataPrivacyClick()'>Data Privacy</a>";

      //Prevent firing drag and onClickMap event when clicking this control
      var stop = L.DomEvent.stopPropagation;
      L.DomEvent
          .on(data_privacy_container, 'click', stop)
          .on(data_privacy_container, 'mousedown', stop)
          .on(data_privacy_container, 'dblclick', stop)
          .on(data_privacy_container, 'click', L.DomEvent.preventDefault);
      return data_privacy_container;
    }
  });
  return control;
}

/**
 * Create User Menu Control on the top left of the map.
 * @param {Array} options List of menu that should be added.
 *
 * Usage: createUserMenuControl(['add', 'download']) to show add-user menu and download menu
 */
function createUserMenuControl(options) {
  var control;
  control = L.Control.extend({
    options: {
      position: 'topleft'
    },
    onAdd: function () {
      // Set HTML and CSS for it
      var user_menu_container = L.DomUtil.create('div',
          'user_menu_control btn-group-vertical');

      if (options.indexOf('add') != -1)
        user_menu_container.innerHTML += $("#user-menu-add-button").html();

      if (options.indexOf('edit') != -1)
        user_menu_container.innerHTML += $("#user-menu-edit-button").html();

      if (options.indexOf('api') != -1)
        user_menu_container.innerHTML += $("#user-menu-api-button").html();

      //Prevent firing drag and onClickMap event when clicking this control
      var stop = L.DomEvent.stopPropagation;
      L.DomEvent
          .on(user_menu_container, 'click', stop)
          .on(user_menu_container, 'mousedown', stop)
          .on(user_menu_container, 'dblclick', stop)
          .on(user_menu_container, 'click', L.DomEvent.preventDefault);
      return user_menu_container
    }
  });
  return control;
}

/**
 * Create legend control instance on the bottom right of the map.
 *
 * @returns {object} control
 */
function createLegendControl(){
  var control;
  control = L.Control.extend({
    options: {
      position: 'bottomright'
    },
    onAdd: function () {
      var legend_container = L.DomUtil.create('div', 'info legend');
      legend_container.innerHTML += $("#legend").html();

      //Prevent firing drag and onClickMap event when clicking this control
      var stop = L.DomEvent.stopPropagation;
      L.DomEvent
          .on(legend_container, 'click', stop)
          .on(legend_container, 'mousedown', stop)
          .on(legend_container, 'dblclick', stop)
          .on(legend_container, 'click', L.DomEvent.preventDefault);
      return legend_container;
    }
  });
  return control;
}

/**
 * Create filter control instance on the top right of the map.
 *
 * @returns {object} control
 */
function createFilterControl() {
  var control;
  control = L.Control.extend({
    options: {
      position: 'topright'
    },
    onAdd: function () {
      var filter_container = L.DomUtil.create('div', 'filter-menu filter');
      filter_container.innerHTML += $("#role-filter").html();

      //Prevent firing drag and onClickMap event when clicking this control
      var stop = L.DomEvent.stopPropagation;
      L.DomEvent
          .on(filter_container, 'mousedown', stop)
          .on(filter_container, 'dblclick', stop);
      return filter_container;
    }
  });
  return control;
}


/**
 * Open an information modal. There is only one modal to use for showing information.
 * This function should be used if there is no other specific behaviour about the modal.
 * Element #information_modal is declared in base.html.
 * @param info_title The title of the modal (usually set as 'Information').
 * @param info_content The content of information.
 */
function showInformationModal(info_title, info_content) {
  var $information_modal = $('#information-modal');
  $information_modal.find('.modal-title').html(info_title);
  $information_modal.find('#info_content').html(info_content);
  $information_modal.modal({
    backdrop: false
  });
}
