"use strict";
class MiriAnalytics {
    constructor() {
        this.isInit = false;
        this.source = '';
        this.maHost = "https://analytics-develop.miridih.com";
    }
    init(source, maHost) {
        var _a, _b;
        if (this.isInit) {
            return;
        }
        this.source = source;
        this.maHost = maHost;
        if (!navigator.sendBeacon) {
            return;
        }
        navigator.sendBeacon = this.makeBeaconProxy();
        this.sessionId = (_a = MiriAnalytics.getCookie(MiriAnalytics.SESSION_COOKIE_NAME)) !== null && _a !== void 0 ? _a : undefined;
        this.deviceId = (_b = MiriAnalytics.getCookie(MiriAnalytics.DEVICE_COOKIE_NAME)) !== null && _b !== void 0 ? _b : undefined;
        if ('undefined' === this.deviceId) {
            this.deviceId = undefined;
            MiriAnalytics.deleteCookie(MiriAnalytics.DEVICE_COOKIE_NAME);
            this.sessionId = undefined;
            MiriAnalytics.deleteCookie(MiriAnalytics.SESSION_COOKIE_NAME);
        }
        else if ('undefined' === this.sessionId) {
            this.sessionId = undefined;
            MiriAnalytics.deleteCookie(MiriAnalytics.SESSION_COOKIE_NAME);
        }
        if (this.sessionId) {
            this.sessionExpiresTime = MiriAnalytics.getExpiresTime(MiriAnalytics.SESSION_COOKIE_NAME);
        }
        this.isInit = true;
    }
    static deleteCookie(name) {
        const host = location.host;
        const domain = host.replace(/^([^.]+)/, '');
        const expires = 'expires=Thu, 01 Jan 1970 00:00:00 GMT';
        document.cookie = name + "=;" + expires + ";path=/;" + "domain=" + domain + ";";
    }
    makeBeaconProxy() {
        const getCoreData = this.getCoreData.bind(this);
        const sendGenericEvent = this.sendGenericEvent.bind(this);
        const getSessionInfo = this.getSessionInfo.bind(this);
        return new Proxy(navigator.sendBeacon, {
            apply(target, thisArg, argArray) {
                const url = argArray[0];
                if (!url.startsWith('https://analytics.google.com')) {
                    return Reflect.apply(target, thisArg, argArray);
                }
                const fullData = (url + (argArray[1] ? ('\n' + argArray[1]) : ''));
                const genericEvents = fullData.split(/_et|\r\n|\n/g).filter(event => event.includes('log_type'));
                for (const event of genericEvents) {
                    const params = new URLSearchParams(event);
                    const eventData = {};
                    for (const entry of params.entries()) {
                        const key = entry[0];
                        const isEpn = key.split(/(epn?\.)/)[1] === 'epn.';
                        const realKeyName = key.split(/(epn?\.)/)[2];
                        if (!realKeyName || 'log_type' === realKeyName) {
                            continue;
                        }
                        eventData[realKeyName] = isEpn ? Number(entry[1]) : entry[1];
                    }
                    const data = Object.assign({ core: getCoreData(), data: {
                            logType: params.get("ep.log_type"),
                            details: eventData
                        } }, getSessionInfo());
                    sendGenericEvent(data);
                }
                return Reflect.apply(target, thisArg, argArray);
            }
        });
    }
    sendPageView(url, referer) {
        const data = {
            core: this.getCoreData(),
            data: {
                url: url || location.href,
                referer: referer || document.referrer,
                title: document.title
            }
        };
        this.sendDataWithSessionData('/track-page-view', data)
            .then((response) => {
            if (response.ok) {
                this.manageSession(response.headers);
            }
        });
    }
    sendGenericEvent(data) {
        try {
            const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
            navigator.sendBeacon(`${this.maHost}/generic-event`, blob);
        }
        catch (e) {
            console.error(e);
            navigator.sendBeacon(`${this.maHost}/generic-event`, JSON.stringify(data));
        }
        if (data.sid) {
            this.setCookie(MiriAnalytics.SESSION_COOKIE_NAME, data.sid);
        }
        if (data.did) {
            this.setCookie(MiriAnalytics.DEVICE_COOKIE_NAME, data.did);
        }
        setTimeout(() => {
            this.manageSession();
        }, 5000);
    }
    getCoreData() {
        return {
            source: this.source,
            url: location.href,
            referer: document.referrer,
            agent: {
                language: navigator.language,
                userAgent: navigator.userAgent,
            },
            display: {
                browserWidth: window.innerWidth,
                browserHeight: window.innerHeight,
                screenWidth: screen.width,
                screenHeight: screen.height,
                screenColorDepth: screen.colorDepth
            }
        };
    }
    sendDataWithSessionData(url, data) {
        return fetch(this.maHost + url, {
            mode: 'cors',
            credentials: 'include',
            method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json',
            }),
            body: JSON.stringify(Object.assign(data, this.getSessionInfo()))
        });
    }
    getSessionInfo() {
        var _a;
        let isSessionValid = (this.sessionId && this.sessionExpiresTime && this.sessionExpiresTime > new Date());
        if (!isSessionValid) {
            const sidFromCookie = MiriAnalytics.getCookie(MiriAnalytics.SESSION_COOKIE_NAME);
            if (sidFromCookie !== null) {
                this.sessionId = sidFromCookie;
                isSessionValid = true;
            }
        }
        if (!this.deviceId) {
            const didFromCookie = MiriAnalytics.getCookie(MiriAnalytics.DEVICE_COOKIE_NAME);
            if (didFromCookie) {
                this.deviceId = didFromCookie;
            }
        }
        return {
            sid: isSessionValid ? this.sessionId : undefined,
            did: (_a = this.deviceId) !== null && _a !== void 0 ? _a : undefined
        };
    }
    manageSession(headers) {
        var _a, _b;
        if (headers) {
            this.sessionId = (_a = headers.get('Session-Id')) !== null && _a !== void 0 ? _a : this.sessionId;
            if (this.sessionId) {
                this.setCookie(MiriAnalytics.SESSION_COOKIE_NAME, this.sessionId);
            }
            this.deviceId = (_b = headers.get('Device-Id')) !== null && _b !== void 0 ? _b : this.deviceId;
            if (this.deviceId) {
                this.setCookie(MiriAnalytics.DEVICE_COOKIE_NAME, this.deviceId);
            }
        }
        if (this.sessionRenewalTimerId) {
            clearTimeout(this.sessionRenewalTimerId);
        }
        this.sessionRenewalTimerId = setTimeout(() => {
            this.sendRenewalSession();
            this.sessionRenewalTimerId = undefined;
            this.manageSession();
        }, MiriAnalytics.SESSION_TIMEOUT);
    }
    setCookie(cname, cvalue) {
        const host = location.host;
        const domain = host.replace(/^([^.]+)/, '');
        const expiresTime = MiriAnalytics.getExpiresTime(cname);
        if (MiriAnalytics.SESSION_COOKIE_NAME === cname) {
            this.sessionExpiresTime = expiresTime;
        }
        const expires = "expires=" + expiresTime.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/;" + "domain=" + domain + ";";
    }
    static getExpiresTime(cookieName) {
        const expiresTime = new Date();
        if (MiriAnalytics.SESSION_COOKIE_NAME === cookieName) {
            expiresTime.setTime(expiresTime.getTime() + MiriAnalytics.SESSION_TIMEOUT);
        }
        else {
            expiresTime.setTime(expiresTime.getTime() + MiriAnalytics.DEVICE_TIMEOUT);
        }
        return expiresTime;
    }
    static getCookie(name) {
        const match = document.cookie.match(RegExp('(?:^|;\\s*)' + (name) + '=([^;]*)'));
        return match ? match[1] : null;
    }
    sendRenewalSession() {
        const data = {
            core: this.getCoreData(),
            data: {}
        };
        return this.sendDataWithSessionData('/session-renewal', data)
            .then((response) => this.manageSession(response.headers));
    }
}
MiriAnalytics.SESSION_COOKIE_NAME = 'ma_sid';
MiriAnalytics.DEVICE_COOKIE_NAME = 'ma_did';
MiriAnalytics.SESSION_TIMEOUT = 30 * 60 * 1000;
MiriAnalytics.DEVICE_TIMEOUT = 63072000000;
var ma = (ma && ma instanceof MiriAnalytics) ? ma : new MiriAnalytics();
