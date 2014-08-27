/**
 * Author: Akbar Gumbira (akbargumbira@gmail.com)
 * Description:
 * This file contains all the function regarding to state user menu control.
 * It follows Airbnb Javascript style guide (https://github.com/airbnb/javascript)
 * and JSDoc for the documentation.
 */

/**
 * Activate Default State. The state when nothing in user menu is clicked
 */
function activateDefaultState() {
  current_mode = DEFAULT_MODE; // Change mode to default
  map.off('click', onMapClick); // Stop onMapclick listener
  $('#map').removeAttr('style'); // Remove all dynamic style to default one
  $('#add-user-button').removeClass('active');
  $('#edit-user-button').removeClass('active');
  $('#delete-user-button').removeClass('active');
  $('#download-button').removeClass('active');
  $('#reminder-button').removeClass('active');
  // If estimated_location_circle exists, remove that circle from map
  if (typeof estimated_location_circle != 'undefined') {
    map.removeLayer(estimated_location_circle);
  }
}

/**
 * Activate Add User State. The state when user click 'Add Me' button
 * @property locate
 */
function activateAddUserState() {
  // Reset to Default State first
  activateDefaultState();
  // Set current mode to add user mode
  current_mode = ADD_USER_MODE;
  // Set css button to active
  $('#add-user-button').addClass('active');
  //Process here:
  // Change cursor to crosshair
  $('#map').css('cursor', 'crosshair');
  // When location is found, do onLocationFoud
  map.on('locationfound', onLocationFound)
  // Locate map to location found
  map.locate({setView: true, maxZoom: 16});
  //Set Listener map onClick
  map.on('click', onMapClick)
}

/**
* Activate Edit User State. The state when user click 'Edit User' button
* @property fitBounds
*/
function activateEditUserState() {
  // Reset to Default State first
  activateDefaultState();
  // Set current mode to add user mode
  current_mode = EDIT_USER_MODE;
  // Set css button to active
  $('#edit-user-button').addClass('active');
  //Zoom map to marker:
  map.fitBounds([[edited_user['latitude'], edited_user['longitude']]]);
  // Set Marker to enable dragging
  edited_user_marker.dragging.enable();
  // Give user the information:
  var info_title = 'Information';
  var info_content = 'Drag your marker and click Done to change your location!';
  showInformationModal(info_title, info_content);
  //Popup the form
  edited_user_marker.bindPopup(edited_user_form_popup).openPopup();
}

/**
 * Activate Delete User State. The state when user click delete button
 */
function activateDeleteUserState() {
  // Reset to Default State first
  activateDefaultState();
  // Set current mode to add user mode
  current_mode = DELETE_USER_MODE;
  // Set css button to active
  $('#delete-user-button').addClass('active');
  // Prompt confirmation to delete:
  $('#delete-confirmation-modal').modal({
    backdrop: false
  });

}

/**
 * Activate Download State. The state when user click download data button
 */
function activateDownloadState() {
  // Reset to Default State first
  activateDefaultState();
  // Set mode to delete user mode
  current_mode = DOWNLOAD_MODE;
  // Set css button to active
  $('#download-button').addClass('active');
  //Process here:
  window.open('/download', '_self');
  activateDefaultState();
}

/**
 * Activate Reminder State. The state when user click reminder button
 */
function activateReminderState() {
  // Reset to Default State first
  activateDefaultState();
  $('#email_reminder').parent().removeClass('has-error');
  // Set mode to delete user mode
  current_mode = REMINDER_MODE;
  // Set css button to active
  $('#reminder-button').addClass('active');
  // Open modal:
  $('#reminder-menu-modal').modal({
    backdrop: false
  });
}
