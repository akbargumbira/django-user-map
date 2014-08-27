/**
 * Author: Akbar Gumbira (akbargumbira@gmail.com)
 * Description: This file contains all utilities function for user map.
 * It follows Airbnb Javascript style guide (https://github.com/airbnb/javascript)
 * and JSDoc for the documentation.
 */

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

/**
 * Return user icon based on user role.
 * @param user_role The role.
 */
function getUserIcon(user_role) {
  var role_icon;
  if (user_role == USER_ROLE) {
    role_icon = user_icon;
  } else if (user_role == TRAINER_ROLE) {
    role_icon = trainer_icon;
  } else if (user_role == DEVELOPER_ROLE) {
    role_icon = developer_icon;
  }
  return role_icon;
}

/**
 * Get User Layer that has been declared based on the role.
 * @param role The user role.
 */
function getUserLayer(role) {
  var layer;
  if (role == USER_ROLE) {
    layer = users_layer;
  } else if (role == TRAINER_ROLE) {
    layer = trainers_layer;
  } else if (role == DEVELOPER_ROLE) {
    layer = developers_layer;
  }
  return layer;
}

/**
 * Return user form based on user attribute.
 * @param user The associative array containing each value of user attribute.
 * @param mode The mode, either ADD_USER_MODE or EDIT_USER_MODE
 */
function getUserForm(user, mode) {
  var form_content = $('#user_form_content').html();
  var $form = $('<div>' + form_content + '</div>');

  /**
   * Set latitude and longitude value, whatever the mode!
   * If it's from the new marker, before passing to this form,
   * that marker location should be added to user attributes
   */
  $form.find('input[type=text]#lat').attr('value', user['latitude']);
  $form.find('input[type=text]#lng').attr('value', user['longitude']);

  if (mode == ADD_USER_MODE) {
    // Set onclick attribute on button
    $form.find(':button#submit_form').attr('onclick', 'addUser();');
    $form.find(':button#cancel_form').attr('onclick', 'cancelAddUser();');
  } else if (mode == EDIT_USER_MODE) {
    // Set name value
    $form.find('input[type=text]#name').attr('value', user['name']);
    // Set email value and set to readonly
    $form.find('input[type=email]#email').attr('value', user['email']);
    $form.find('input[type=email]#email').attr('readonly', true);
    // Set website value
    $form.find('input[type=url]#website').attr('value', user['website']);
    // Checked one of the radio option of Role
    if (user['role'] == USER_ROLE) {
      $form.find('input[type=radio][name=role]:nth(0)').attr('checked', true);
    } else if (user['role'] == TRAINER_ROLE) {
      $form.find('input[type=radio][name=role]:nth(1)').attr('checked', true);
    } else if (user['role'] == DEVELOPER_ROLE) {
      $form.find('input[type=radio][name=role]:nth(2)').attr('checked', true);
    }
    // Checked email updates checkbox if the user should get email updates
    if (user['email_updates']) {
      $form.find('input[type=checkbox]#email_updates').attr('checked', true);
    }
    // Set latitude and longitude value
    $form.find('input[type=text]#lat').attr('value', user['latitude']);
    $form.find('input[type=text]#lng').attr('value', user['longitude']);
    // Set onclick attribute on button:
    $form.find(':button#submit_form').attr('onclick', 'editUser();');
    $form.find(':button#cancel_form').attr('onclick', 'cancelEditUser();');
  }
  return $form.html().toString();
}

/**
 * Get Popup containing user form.
 * @param user The javascript associative array representing user.
 * @param mode The mode, either ADD_USER_MODE or EDIT_USER_MODE.
 * @returns L.popup()
 */
function getUserFormPopup(user, mode) {
  var form = getUserForm(user, mode);
  var popup = L.popup({closeButton: false});
  popup.setContent(form);
  return popup;
}
