// user/static/user/js/social_login.js


function buildQuery(params) {
    return Object.keys(params).map(function (key) {return key + '=' + encodeURIComponent(params[key])}).join('&')
}
function buildUrl(baseUrl, queries) {
    return baseUrl + '?' + buildQuery(queries)
}

function naverLogin() { // 네이버 로그인
    params = {
        response_type: 'code',
        client_id:'QLgsSPeOhI9_FpC6MOY5',
        redirect_uri: location.origin + '/user/login/social/naver/callback/',
        state: document.querySelector('[name=csrfmiddlewaretoken]').value
    }
    url = buildUrl('https://nid.naver.com/oauth2.0/authorize', params)
    location.replace(url)
}
