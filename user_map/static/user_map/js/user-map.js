/**
 * Author: Akbar Gumbira (akbargumbira@gmail.com)
 * Description:
 * This file contains methods related directly to user map.
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
 * Create leaflet icon marker.
 *
 * @param {string} icon_path The icon path.
 * @param {string} shadow_path The shadow path.
 * @return {IconMarkerBase} icon_marker
 */
function createIconMarker(icon_path, shadow_path) {
  var IconMarkerBase = createIconMarkerBase(shadow_path);
  return new IconMarkerBase({iconUrl: icon_path});
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

      if (options.indexOf('delete') != -1)
        user_menu_container.innerHTML += $("#user-menu-delete-button").html();

      if (options.indexOf('download') != -1)
        user_menu_container.innerHTML += $("#user-menu-download-button").html();

      if (options.indexOf('forgot') != -1)
        user_menu_container.innerHTML += $("#user-menu-forgot-button").html();

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
