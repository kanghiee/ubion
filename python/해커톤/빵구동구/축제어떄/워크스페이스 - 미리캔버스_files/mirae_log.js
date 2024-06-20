var mi_chat_adkey = '';
var mi_cfg = null;
function mi_sett(){
	var scripts = document.getElementsByTagName('script');
	for(i in scripts){
		var script = scripts[i];
		if(typeof script.src =='undefined' || script.src == '') continue;
		if (script.src.indexOf("mirae_log_chat_common.js") !== -1 || script.src.indexOf("mirae_log_chat_common_dev.js") !== -1){
			var tmp = script.src.split('?')[1];
			if(typeof tmp !== 'undefined'){
				tmp = tmp.split('&');
				for(var i=0; i< tmp.length; i++){
					var new_tmp = tmp[i].split('=');
					if(new_tmp[0] == 'adkey') mi_chat_adkey = new_tmp[1];
				}
			}
		}
	}
	if(mi_chat_adkey == '' && typeof mi_adkey != 'undefined' && mi_adkey != ''){
		mi_chat_adkey = mi_adkey;
	}
	var cfg	= {
		dev:false,
		load:{},
		use:{analysis:true,mitalk:true,click:true},
		url:{
			l4:'//log1.toup.net',
			response:'mirae_response.php',
			act:'/mirae_log_chat_act.js',
			mitalk:'//www.miraetalk.com',
			mitalk_log:'//log.miraetalk.com',
			map:'//map.toup.net'
		}
	}
	if(cfg.dev){
		cfg.url.response = 'mirae_response_dev.php';
		cfg.url.act = '/mirae_log_chat_act_dev.js';
		cfg.url.mitalk = '//106.10.49.216:3000';
	}

	if(typeof this.use!=='undefined'){
		if(typeof this.use.analysis!=='undefined'){
			cfg.use.analysis = this.use.analysis;
		}
		if(typeof this.use.mitalk!=='undefined'){
			cfg.use.mitalk = this.use.mitalk;
		}
		if(typeof this.use.click!=='undefined'){
			cfg.use.click = this.use.click;
		}
	}
	return cfg;
}
function insert_before(el){
	if(typeof el.src == 'undefined' || el.src == ''){
		return;
	}
	var script,target;
	var scripts = document.getElementsByTagName('script');
	for( k in scripts){
		var s = scripts[k];
		if(typeof s.src =='undefined' || s.src == '') continue;
		if(s.src.indexOf(el.src) !== -1){
			return;
		}
	}	
	script = document.createElement('script');
	script.type	= 'text/javascript';
	if(typeof el.async == 'undefined' || el.async == false){
		script.defer = !0;
	}else{
		script.async = !0;
	}
	script.src = el.src;
	if(typeof el.callback !=='undefined'){ 
		script.onload = el.callback;
	}
	if(typeof el.target == 'undefined'){	
		target = document.getElementsByTagName("script")[0];
		if(typeof target == 'undefined'){
			target = document.head;
		}
	}else{
		target = el.target;
	}
	target.parentNode.insertBefore(script,target);
}
(function(){
	mi_cfg = mi_sett.apply(null);
	insert_before({src:'//log1.toup.net/mirae_response_load.php?k='+mi_chat_adkey,callback:function(){ 
		console.log(mi_load_return);
		mi_chat_adkey = mi_load_return.mi_adkey;
		mi_cfg.load = mi_load_return;
		mi_dt=new Date(),mi_y=mi_dt.getFullYear(),mi_m=mi_dt.getMonth()+1,mi_d=mi_dt.getDate(),mi_h=mi_dt.getHours();
		mi_date=""+mi_y+(mi_m<=9?"0":"")+mi_m+(mi_d<=9?"0":"")+mi_d+(mi_h<=9?"0":"")+mi_h;
		if(mi_load_return.flag!='N'){
			insert_before({src:mi_cfg.url.l4+"/mirae_log_chat_act.js?t="+mi_date});
		}
	}});
})();