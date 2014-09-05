/**
 * Author: Akbar Gumbira (akbargumbira@gmail.com)
 * Description:
 * This file contains all the function to prepare map components.
 * It follows Airbnb Javascript style guide (https://github.com/airbnb/javascript)
 * and JSDoc for the documentation.
 */

/**
 * Create basemap instance to be used.
 * @param {string} url The URL for the tiles layer
 * @param {string} attribution The attribution of the layer
 * @property tileLayer
 * @returns {object} base_map
 */
function createBasemap(url, attribution) {
  var base_map;
  base_map = L.tileLayer(url, {
    attribution: attribution,
    maxZoom: 18
  });
  return base_map;
}

/**
 * Create IconMarkerBase that will be used for icon marker.
 * @param {string} shadow_icon_path The path to shadow icon.
 * @returns {object} IconMarkerBase
 * @property Icon
 */
function createIconMarkerBase(shadow_icon_path) {
  var IconMarkerBase;
  IconMarkerBase = L.Icon.extend({
    options: {
      shadowUrl: shadow_icon_path,
      iconSize: [19, 32],
      shadowSize: [42, 35],
      iconAnchor: [12, 32],
      shadowAnchor: [12, 32],
      popupAnchor: [-2, -32]
    }
  });
  return IconMarkerBase;
}

/**
 * Create all icons that are used.
 * @param {string} user_icon_path The icon path for user role.
 * @param {string} trainer_icon_path The icon path for trainer role.
 * @param {string} developer_icon_path The icon path for developer role.
 * @param {string} shadow_icon_path The shadow for all icons.
 * @returns {{user_icon: IconMarkerBase, trainer_icon: IconMarkerBase, developer_icon: IconMarkerBase}}
 */
function createAllIcons(user_icon_path, trainer_icon_path, developer_icon_path, shadow_icon_path) {
  var IconMarkerBase = createIconMarkerBase(shadow_icon_path);
  var user_icon = new IconMarkerBase({iconUrl: user_icon_path});
  var trainer_icon = new IconMarkerBase({iconUrl: trainer_icon_path});
  var developer_icon = new IconMarkerBase({iconUrl: developer_icon_path});
  var all_icons;
  all_icons = {
    user_icon: user_icon,
    trainer_icon: trainer_icon,
    developer_icon: developer_icon
  };
  return all_icons;
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
 * @param {object} options Visibility of each component.
 * False if hidden, True if visible. If None, then it will be hidden.
 *
 * There are 3 menus on this control:
 * 1. add-user-menu
 * 2. edit-user-menu
 * 3. delete-user-menu
 * 4. download-menu
 * 5. reminder-menu
 *
 * Usage: initializeUserMenuControl({"add-user-menu": true, "download-menu": true})
 * to show add-user-menu and download-menu
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
      if (options['add-user-menu']) {
        user_menu_container.innerHTML += $("#user-menu-add-button").html();
        onAddUserButtonClick = function () {
          if (current_mode != ADD_USER_MODE) {
            activateAddUserState();
          }
        };
      }
      if (options['edit-user-menu']) {
        user_menu_container.innerHTML += $("#user-menu-edit-button").html();
        onEditUserButtonClick = function () {
          if (current_mode != EDIT_USER_MODE) {
            activateEditUserState();
          }
        };
      }
      if (options['delete-user-menu']) {
        user_menu_container.innerHTML += $("#user-menu-delete-button").html();
        onDeleteUserButtonClick = function () {
          if (current_mode != DELETE_USER_MODE) {
            activateDeleteUserState();
          }
        };
      }
      if (options['download-menu']) {
        user_menu_container.innerHTML += $("#user-menu-download-button").html();
        onDownloadButtonClick = function () {
          if (current_mode != DOWNLOAD_MODE) {
            activateDownloadState();
          }
        };
      }
      if (options['reminder-menu']) {
        user_menu_container.innerHTML += $("#user-menu-reminder-button").html();
        onReminderButtonClick = function () {
          if (current_mode != REMINDER_MODE) {
            activateReminderState();
          }
        };
      }

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
 * The legend contains the icon and the name of the role:
 * 1. User
 * 2. Trainer
 * 3. Developer
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
      var legend_container = L.DomUtil.create('div',
          'info legend');
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
 * Listener to geolocation. Called when location is found.
 * NOTE:
 * Bind label to circle/circle marker is not working.
 * See the issue here: https://github.com/Leaflet/Leaflet.label/issues/31
 * @param e
 */
function onLocationFound(e) {
  var radius = e.accuracy / 2;
  var label = "You are within " + radius + " meters from this point";
  // If estimated_location_circle exists, remove that circle first from map
  if (typeof estimated_location_circle != 'undefined') {
    map.removeLayer(estimated_location_circle);
  }
  estimated_location_circle = L.circle(
      e.latlng, radius, {clickable: false, fillOpacity: 0.1}
  );
  estimated_location_circle.bindLabel(label, {noHide: true}).addTo(map);
}

/**
 * Listener when map is clicked.
 * @param e
 */
function onMapClick(e) {
  // Clear the un-saved clicked marker
  if (marker_new_user != null) {
    cancelMarker();
  }
  //Get new marker
  var markerLocation = e.latlng;
  marker_new_user = L.marker(markerLocation);
  map.addLayer(marker_new_user);
  var wrappedLocation = L.latLng(markerLocation.lat, markerLocation.lng).wrap()
  var user = {
    'latitude': wrappedLocation.lat.toFixed(8),
    'longitude': wrappedLocation.lng.toFixed(8)
  };
  var popup = getUserFormPopup(user, ADD_USER_MODE);
  marker_new_user.bindPopup(popup).openPopup()
}

/**
 * Cancel new user marker from the map.
 */
function cancelMarker() {
  map.removeLayer(marker_new_user);
}
