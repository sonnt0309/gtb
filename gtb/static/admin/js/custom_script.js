// templates/admin/login.html
function changeLanguageFormLogin() {
    let selectedLang = $("#languages").val();
    let redirectUrl = window.location.origin + '/' + selectedLang + '/admin/login';
    location.href = redirectUrl;
}

// Content pages (after login)
function changeLanguage() {
    let langToChange = $("#lang-select").val();
    document.getElementById(langToChange).click();
}
function changeLangToUserLocale(urlPathName) {
    let pathNameArr = urlPathName.split('/');
    // Remove emtpy element in array
    pathNameArr = pathNameArr.filter(Boolean);
    if (pathNameArr[pathNameArr.length - 1].toLowerCase() !== 'login') {
        if (!sessionStorage.getItem('isLogged') || sessionStorage.getItem('isLogged')=='false' ) {
            let user_locale = $("#user-locale").val().toLowerCase();
            if (user_locale !== 'en') {
                document.getElementById(user_locale).click();
            }
            sessionStorage.setItem('isLogged', true);
        }
    }
}

// templates/admin/edit_inline/tabular_paginated.html
function changeSumaryLabelTabular() {
    let labelRecord = $('#hidLabelRecord').text();
    let elmnt = document.createElement("span");
    let textnode = document.createTextNode(labelRecord);
    elmnt.appendChild(textnode);
    let item = document.getElementsByClassName("showall")[0];
    item.replaceWith(elmnt, item);
}
function changeSumaryLabelTabularCustom(idBlock) {
    let labelRecord = $('#hidLabelRecord_'+idBlock).text();
    let elmnt = document.createElement("span");
    let textnode = document.createTextNode(labelRecord);
    elmnt.appendChild(textnode);
    let item = document.getElementById(idBlock).getElementsByClassName("showall")[0];
    item.replaceWith(elmnt, item);
}


// templates/admin/includes/fieldset_key.html
function generateNewKey(idInput) {
    let chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
	let string_length = 6;
	let random_string = '';
	for (let i=0; i<string_length; i++) {
		let rnum = Math.floor(Math.random() * chars.length);
		random_string += chars.substring(rnum,rnum+1);
	}
	// Set new key to field input license key
	$("#id_"+idInput).val(random_string)
}
// templates/admin/includes/fieldset_key.html
function generateNewKeyAPi(idInput) {
    let chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
	let string_length = 16;
	let random_string = '';
	for (let i=0; i<string_length; i++) {
		let rnum = Math.floor(Math.random() * chars.length);
		random_string += chars.substring(rnum,rnum+1);
	}
	// Set new key to field input license key
	$("#id_"+idInput).val(random_string)
}

$('select#id_license').on('change', function() {
    let id_license = $("#id_license option:selected").text();
    getUserNameByLicenseId(id_license);
});
function getUserNameByLicenseId(id_license){
    let csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
   let hostName = window.location.origin;
   if(!id_license){
       alert('Error value!')
       return;
   }
   let url = hostName + `/activations/getUserByLicenseId/`+id_license;
        $.ajax({
            url: '' + url,
            type: 'GET',
            success: function (data) {
                let username = data.user.name;
                let userid = data.user.id;
                let link_ref= `/admin/auth/user/${userid}/change/`;
                $("#username_by_licenseId").hide().fadeIn(300);
                $("#username_by_licenseId_value").html(`<a href=${link_ref} target=\"_blank\">${username}</a>`);
            },
            error: function(xhr){
                $("#username_by_licenseId").hide().fadeIn(300);
                $("#username_by_licenseId_value").text('');
                console.log('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
            },
            async: false
        });
}
function csrfSafeMethod(method) {
   // these HTTP methods do not require CSRF protection
   return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$('select#id_activation').on('change', function() {
    let id_activation = $("#id_activation option:selected").text();
    getRelateInfoByActivationKey(id_activation);
});
function getRelateInfoByActivationKey(activate_key){
    let csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
   let hostName = window.location.origin;
   if(!activate_key){
       alert('Error value!')
       return;
   }
   let username = '';
   let url = hostName + `/execution_status/getRelateInfoByActivateKey/`+activate_key;
        $.ajax({
            url: '' + url,
            type: 'GET',
            success: function (data) {
                let username = data.username;
                let license_id = data.license_id;
                let user_url = data.user_url;
                let license_url = data.license_url;
                let user_link_ref= `/admin/auth/user/${user_url}/change/`;
                let license_link_ref= `/admin/license/license/${license_url}/change/`;
                $("#username_by_activationId").hide().fadeIn(100);
                $("#username_by_activationId_value").html(`<a href=${user_link_ref} target=\"_blank\">${username}</a>`);
                $("#licenseId_by_activationId").hide().fadeIn(100);
                $("#licenseId_by_activationId_value").html(`<a href=${license_link_ref} target=\"_blank\">${license_id}</a>`);
                $("#pcName_by_activationId").hide().fadeIn(100).text(data.pc_name);
                $("#window_product_id_by_activationId").hide().fadeIn(100).text(data.window_product_id);
                $("#mac_address_by_activationId").hide().fadeIn(100).text(data.mac_address);
                $("#drive_serial_by_activationId").hide().fadeIn(100).text(data.drive_serial_number);
            },
            error: function(xhr){
                $("#username_by_activationId").hide().fadeIn(100);
                $("#username_by_activationId_value").html('');
                $("#licenseId_by_activationId").hide().fadeIn(100);
                $("#licenseId_by_activationId_value").html('');
                $("#pcName_by_activationId").hide().fadeIn(100).text('');
                $("#window_product_id_by_activationId").hide().fadeIn(100).text('');
                $("#mac_address_by_activationId").hide().fadeIn(100).text('');
                $("#drive_serial_by_activationId").hide().fadeIn(100).text('');
                console.log('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
            },
            async: false
        });
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function onDeleteUser(event, id_array) {
    event.preventDefault();

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    let hostName = window.location.origin;
    let currentLang = window.location.pathname.split('/')[1];
    let url = hostName + `/user/delete/`;
        $.ajax({
            url: '' + url,
            type: 'DELETE',
            data: {
                id_array:JSON.stringify(id_array)
            },
            success: function (data) {
                console.log(data);
                if (data.code == 200){
                    location.href = "/admin/auth/user";
                } else {
                     alert(data.code);
                }
            },
            error: function(xhr){
                alert('Error');
                console.log('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
            },
            async: false
        });
}


// templates/registration/logged_out.html
function handleLogout() {
    sessionStorage.setItem('isLogged', false);
}

// If in add page
$(function() {
    let pathName = window.location.pathname;
    let pathNameArr = pathName.split('/').filter(Boolean);
    // Hide created date,
    if(pathNameArr[pathNameArr.length-1].toLowerCase()==='add'){
        if ($(".form-row.field-created_date").length) {
            $(".form-row.field-created_date").hide();
        }
        if ($(".form-row.field-updated_date").length) {
            $(".form-row.field-updated_date").hide();
        }
    }
});

$("#filter_now").click(function(event){
    let title_filter = $("#id_title").val();
    if(!title_filter){
        $("#id_title").val("#")
    }
    $("#id_title").css("color","transparent");
});

// Function to get query params.
//  Example URL: localhost:8000/?_afilter=49
//  Input: _afilter -- let _afilterParams = getUrlParameter('_afilter')
//  Output: 49 -- _afilterParams = 49
function getUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
};

// advanced_filters/templates/admin/advanced_filters.html
function hideButtonEditWhenAdd(){
    let _afilter = getUrlParameter('_afilter');
    const limit_lenght_for_afilter_id = 15;
    if(_afilter.length > limit_lenght_for_afilter_id){
        $(".object-tools .edit-link").hide();
    }
}