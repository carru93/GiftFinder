/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(n){var e;(e=n&&n.fn&&n.fn.select2&&n.fn.select2.amd?n.fn.select2.amd:e).define("select2/i18n/bs",[],function(){function e(n,e,t,i){return n%10==1&&n%100!=11?e:2<=n%10&&n%10<=4&&(n%100<12||14<n%100)?t:i}return{errorLoading:function(){return"Preuzimanje nije uspijelo."},inputTooLong:function(n){n=n.input.length-n.maximum;return"Obrišite "+n+" simbol"+e(n,"","a","a")},inputTooShort:function(n){n=n.minimum-n.input.length;return"Ukucajte bar još "+n+" simbol"+e(n,"","a","a")},loadingMore:function(){return"Preuzimanje još rezultata…"},maximumSelected:function(n){return"Možete izabrati samo "+n.maximum+" stavk"+e(n.maximum,"u","e","i")},noResults:function(){return"Ništa nije pronađeno"},searching:function(){return"Pretraga…"},removeAllItems:function(){return"Uklonite sve stavke"}}}),e.define,e.require},event=new CustomEvent("dal-language-loaded",{lang:"bs"});document.dispatchEvent(event);
