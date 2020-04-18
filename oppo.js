(function() {
  var docCookies = {
    getItem: function (sKey) {
      return decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(sKey).replace(/[-.+*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
    },
    setItem: function (sKey, sValue, vEnd, sPath, sDomain, bSecure) {
      if (!sKey || /^(?:expires|max\-age|path|domain|secure)$/i.test(sKey)) { return false; }
      var sExpires = "";
      if (vEnd) {
        switch (vEnd.constructor) {
          case Number:
            sExpires = vEnd === Infinity ? "; expires=Fri, 31 Dec 9999 23:59:59 GMT" : "; max-age=" + vEnd;
            break;
          case String:
            sExpires = "; expires=" + vEnd;
            break;
          case Date:
            sExpires = "; expires=" + vEnd.toUTCString();
            break;
        }
      }
      document.cookie = encodeURIComponent(sKey) + "=" + encodeURIComponent(sValue) + sExpires + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "") + (bSecure ? "; secure" : "");
      return true;
    },
    removeItem: function (sKey, sPath, sDomain) {
      if (!sKey || !this.hasItem(sKey)) { return false; }
      document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + ( sDomain ? "; domain=" + sDomain : "") + ( sPath ? "; path=" + sPath : "");
      return true;
    },
    hasItem: function (sKey) {
      return (new RegExp("(?:^|;\\s*)" + encodeURIComponent(sKey).replace(/[-.+*]/g, "\\$&") + "\\s*\\=")).test(document.cookie);
    },
    keys: /* optional method: you can safely remove it! */ function () {
      var aKeys = document.cookie.replace(/((?:^|\s*;)[^\=]+)(?=;|$)|^\s*|\s*(?:\=[^;]*)?(?:\1|$)/g, "").split(/\s*(?:\=[^;]*)?;\s*/);
      for (var nIdx = 0; nIdx < aKeys.length; nIdx++) { aKeys[nIdx] = decodeURIComponent(aKeys[nIdx]); }
      return aKeys;
    }
  };
  
  function s(e) {
    for (var t = 0, o = e.length, n = 5381; t < o; ++t) n += (n << 5) + e.charAt(t).charCodeAt();
    return 2147483647 & n
  }
  
  function getCsrfToken(e) {
    return e = null == e ? "" : s(e);
  }
  
  function sleep(time) {
    return new Promise(resolve => {
      var id = setTimeout(() => {
        clearTimeout(id);
        resolve();
      }, time * 1000);
    });
  }
  
  
  var listurl = 'https://rest-cn01a.ocloud.heytapmobi.com/old-note/v1/list';
  var infourl = 'https://rest-cn01a.ocloud.heytapmobi.com/old-note/v1/info';
  
  function queryData(url) {
    var tokenkey = docCookies.getItem('TOKENKEY');
    var ctoken = getCsrfToken(tokenkey);
    return fetch(url + `&ctoken=${ctoken}&TOKENKEY=${tokenkey}`, {
      method: 'GET',
      credentials: 'include'
    });
  }
  
  
  async function noteData() {
    var last = 0;
    var list = [];
    // 便签内容
    var contentList = [];
    while (true) {
      var resp = await queryData(`${listurl}?last=${last}`);
      var json = await resp.json();
      list = list.concat(json.body.content);
      await sleep(1);
      if (!json.body.final) {
        last = json.body.last;
      } else {
        break;
      }
    }
    for (let note of list) {
      let id = note.noteGuid;
      resp = await queryData(`${infourl}?id=${id}`);
      json = await resp.json();
      contentList.push({
        date: new Date(parseInt(json.body.noteUpdated)),
        content: json.body.content
      });
      await sleep(1);
    }
    
    var filename = '便签.txt';
    var a = document.createElement('a');
    var blob = new Blob([JSON.stringify(contentList)]);
    a.download = filename;
    a.href = URL.createObjectURL(blob);
    a.click();
  }
  
  noteData();
})();
