/* GogoStudio.app — audience measurement after explicit opt-in only. */
(() => {
  "use strict";
  const measurementId = "G-3DPSLCFK10";
  const storageKey = "gogostudio_analytics_consent_v1";
  const expiryMs = 180 * 86400000;
  const wording = {
    fr:["Statistiques de fréquentation","Avec votre accord, Google Analytics mesure les visites, les pages consultées et les clics vers Google Play. Aucun suivi Analytics n'est activé si vous refusez.","Refuser","Accepter","En savoir plus","Gérer les cookies"],
    en:["Audience statistics","With your permission, Google Analytics measures visits, viewed pages and Google Play clicks. No Analytics tracking is enabled if you decline.","Decline","Accept","Learn more","Cookie settings"],
    es:["Estadísticas de visitas","Con tu permiso, Google Analytics mide las visitas, las páginas vistas y los clics hacia Google Play. No se activa si rechazas.","Rechazar","Aceptar","Más información","Configurar cookies"],
    it:["Statistiche delle visite","Con il tuo consenso, Google Analytics misura visite, pagine viste e clic su Google Play. Se rifiuti, non viene attivato.","Rifiuta","Accetta","Informazioni","Gestisci i cookie"],
    de:["Besucherstatistik","Mit Ihrer Einwilligung erfasst Google Analytics Besuche, Seitenaufrufe und Klicks zu Google Play. Ohne Einwilligung ist es deaktiviert.","Ablehnen","Akzeptieren","Mehr erfahren","Cookie-Einstellungen"],
    nl:["Bezoekersstatistieken","Met uw toestemming meet Google Analytics bezoeken, bekeken pagina's en klikken naar Google Play. Zonder toestemming is het uitgeschakeld.","Weigeren","Accepteren","Meer informatie","Cookie-instellingen"],
    pt:["Estatísticas de visitas","Com o seu consentimento, Google Analytics mede visitas, páginas vistas e cliques para o Google Play. Sem consentimento, fica desativado.","Recusar","Aceitar","Saber mais","Gerir cookies"],
    ar:["إحصاءات الزيارات","بموافقتك، يقيس Google Analytics الزيارات والصفحات والنقرات إلى Google Play. لن يتم تفعيله إذا رفضت.","رفض","موافقة","المزيد","إعدادات ملفات الارتباط"],
    ja:["アクセス解析","同意された場合のみ、Google Analyticsで訪問数、閲覧ページ、Google Playへのクリックを計測します。同意しない場合は計測しません。","拒否する","同意する","詳細","Cookie設定"],
    ko:["방문 통계","동의하는 경우에만 Google Analytics로 방문, 페이지 조회, Google Play 클릭을 측정합니다. 거부하면 활성화되지 않습니다.","거부","동의","자세히","쿠키 설정"]
  };
  const packages = {
    "com.gogostudio.stopododo":"store_click_stopododo",
    "com.kama54.easysenior":"store_click_clikospido",
    "com.zapiki.tv":"store_click_zapiki"
  };
  const queryLanguage = new URLSearchParams(location.search).get("lang");
  const language = (queryLanguage || document.documentElement.lang || navigator.language || "fr").toLowerCase().split(/[-_]/)[0];
  const lang = Object.prototype.hasOwnProperty.call(wording, language) ? language : "fr";
  const t = wording[lang], detailsUrl="/mesure-audience.html?lang="+encodeURIComponent(lang);
  let notice=null, started=false, choice=getChoice();

  function getChoice(){
    try{
      const item=JSON.parse(localStorage.getItem(storageKey)||"null");
      if(item && item.until>Date.now() && ["accept","reject"].includes(item.value))return item.value;
    }catch(e){}
    return null;
  }
  function store(value){
    choice=value;
    try{localStorage.setItem(storageKey,JSON.stringify({value,until:Date.now()+expiryMs}));}catch(e){}
  }
  function enable(){
    if(started || choice!=="accept")return;
    started=true;
    window.dataLayer=window.dataLayer||[];
    window.gtag=window.gtag||function(){window.dataLayer.push(arguments);};
    window.gtag("consent","default",{analytics_storage:"granted",ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied"});
    window.gtag("js",new Date());
    window.gtag("config",measurementId,{allow_google_signals:false,allow_ad_personalization_signals:false,cookie_expires:395*86400,send_page_view:true});
    const script=document.createElement("script");
    script.async=true;
    script.src="https://www.googletagmanager.com/gtag/js?id="+encodeURIComponent(measurementId);
    document.head.appendChild(script);
  }
  function forgetCookies(){
    const host=location.hostname, domain=host.split(".").slice(-2).join(".");
    document.cookie.split(";").forEach(pair=>{
      const name=pair.trim().split("=")[0];
      if(!/^_ga(?:_|$)/.test(name))return;
      ["","; domain="+host,"; domain=."+domain].forEach(d=>{
        document.cookie=name+"=; Max-Age=0; path=/; SameSite=Lax"+d;
      });
    });
  }
  function decide(value){
    const wasStarted=started;
    store(value);
    if(notice){notice.remove();notice=null;}
    if(value==="accept")enable();
    else if(wasStarted){forgetCookies();location.reload();}
  }
  function element(tag,cls,label){
    const node=document.createElement(tag);
    if(cls)node.className=cls;
    if(label)node.textContent=label;
    return node;
  }
  function show(){
    if(notice){notice.querySelector(".gg-analytics-reject").focus();return;}
    notice=element("section","gg-analytics-notice");
    notice.setAttribute("role","region");
    notice.setAttribute("aria-label",t[0]);
    if(lang==="ar")notice.dir="rtl";
    const heading=element("strong","gg-analytics-heading",t[0]);
    const description=element("p","gg-analytics-description",t[1]);
    const info=element("a","gg-analytics-info",t[4]);info.href=detailsUrl;
    const buttons=element("div","gg-analytics-buttons");
    const reject=element("button","gg-analytics-button gg-analytics-reject",t[2]);
    reject.type="button";reject.addEventListener("click",()=>decide("reject"));
    const accept=element("button","gg-analytics-button gg-analytics-accept",t[3]);
    accept.type="button";accept.addEventListener("click",()=>decide("accept"));
    buttons.append(reject,accept);
    notice.append(heading,description,info,buttons);
    document.body.appendChild(notice);
  }
  function init(){
    const style=document.createElement("style");
    style.textContent=[
      ".gg-analytics-notice,.gg-analytics-notice *{box-sizing:border-box!important}",
      ".gg-analytics-notice{position:fixed!important;bottom:12px!important;left:50%!important;transform:translateX(-50%)!important;z-index:2147483600!important;width:min(620px,calc(100vw - 24px))!important;max-height:65vh!important;overflow:auto!important;padding:20px!important;background:#fff!important;color:#192338!important;border:1px solid #cbd5e1!important;border-radius:14px!important;box-shadow:0 10px 30px #0005!important;font:15px/1.5 system-ui,sans-serif!important}",
      ".gg-analytics-heading{display:block!important;margin-bottom:8px!important;font:bold 17px/1.35 system-ui,sans-serif!important}",
      ".gg-analytics-description{margin:0 0 8px!important;font:14px/1.5 system-ui,sans-serif!important;color:#283449!important}",
      ".gg-analytics-info{display:inline-block!important;margin-bottom:14px!important;color:#174ea6!important;text-decoration:underline!important;font:600 14px/1.4 system-ui,sans-serif!important}",
      ".gg-analytics-buttons{display:flex!important;gap:12px!important;flex-wrap:wrap!important}",
      ".gg-analytics-button{flex:1 1 130px!important;min-height:44px!important;border:2px solid #243858!important;border-radius:8px!important;background:#243858!important;color:#fff!important;padding:10px!important;font:bold 15px system-ui,sans-serif!important;cursor:pointer!important}",
      ".gg-analytics-button:focus-visible,.gg-analytics-settings:focus-visible{outline:3px solid #3875e8!important;outline-offset:3px!important}",
      ".gg-analytics-settings-wrap{text-align:center!important;padding:12px!important}",
      ".gg-analytics-settings{border:1px solid currentColor!important;border-radius:5px!important;background:transparent!important;color:inherit!important;padding:5px 9px!important;font:500 13px system-ui,sans-serif!important;cursor:pointer!important}"
    ].join("");
    document.head.appendChild(style);
    const footer=document.querySelector("footer");
    const wrap=element("div","gg-analytics-settings-wrap");
    const settings=element("button","gg-analytics-settings",t[5]);
    settings.type="button";settings.addEventListener("click",show);
    wrap.appendChild(settings);
    (footer||document.body).appendChild(wrap);
    if(!footer){wrap.style.cssText="position:fixed;right:4px;bottom:0;z-index:2147483500;background:#243858;color:#fff";}
    if(choice===null)show();
    if(choice==="accept")enable();
    document.addEventListener("click",event=>{
      if(!started||choice!=="accept")return;
      const link=event.target.closest&&event.target.closest("a[href]");
      if(!link)return;
      try{
        const url=new URL(link.href,location.href);
        if(url.hostname!=="play.google.com"||url.pathname!=="/store/apps/details")return;
        const eventName=packages[url.searchParams.get("id")];
        if(eventName&&typeof window.gtag==="function")window.gtag("event",eventName,{link_url:url.href,transport_type:"beacon"});
      }catch(e){}
    },true);
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init,{once:true});else init();
})();