function loneToMainContent() {
    if ($('#lone-spinner').length && $('#main-content').length) {
        $('#lone-spinner').hide();
        $('#main-content').show();
    }
}

function basicStatusChangeCallback(response) {
    if (response.status === 'connected') {
        // Logged into your app and Facebook
        $.post('/svc/auth/login', response.authResponse, function(success) {
            if (success === true) {
                loneToMainContent();
            } else {
                console.log('fail from auth');
                $.post('/svc/auth/logout');
                window.location = '/';
            }
        });
    } else {
        console.log('not logged in to fb');
        $.post('/svc/auth/logout');
        window.location = '/';
    }
}

function openLoginDialog() {
    FB.login(function(response) {
        // implemented by html scripts if anything needs to happen
        if (typeof statusChangeCallback == 'function') {
            statusChangeCallback(response);
        }
    }, {scope: 'public_profile,email'});
}

function checkLoginState() {
    FB.getLoginStatus(function(response) {
        // implemented by html scripts if anything needs to happen
        if (typeof statusChangeCallback == 'function') {
            statusChangeCallback(response);
        } else {
            basicStatusChangeCallback(response);
        }
    });
}

window.fbAsyncInit = function() {
    FB.init({
    appId      : '617235401742568',
    cookie     : true,  // enable cookies to allow the server to access
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.2' // use version 2.2
    });

    checkLoginState();
};

// Load the SDK asynchronously
(function(d, s, id) {
var js, fjs = d.getElementsByTagName(s)[0];

if (d.getElementById(id)) return;
js = d.createElement(s); js.id = id;
js.src = "//connect.facebook.net/en_US/sdk.js";
fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
